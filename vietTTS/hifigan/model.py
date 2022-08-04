import haiku as hk
import jax
import jax.numpy as jnp

LRELU_SLOPE = 0.1


def get_padding(kernel_size, dilation=1):
  p = int((kernel_size * dilation - dilation) / 2)
  return ((p, p), )


class ResBlock1(hk.Module):
  def __init__(self, h, channels, kernel_size=3, dilation=(1, 3, 5), name="resblock1"):
    super().__init__(name=name)

    self.h = h
    self.convs1 = [
        hk.Conv1D(channels, kernel_size, 1, rate=dilation[i], padding=get_padding(
            kernel_size, dilation[i]), name=f'convs1_{i}')
        for i in range(3)
    ]

    self.convs2 = [
        hk.Conv1D(channels, kernel_size, 1, rate=1, padding=get_padding(kernel_size, 1), name=f"convs2_{i}")
        for i in range(3)
    ]

  def __call__(self, x):
    for c1, c2 in zip(self.convs1, self.convs2):
      xt = jax.nn.leaky_relu(x, LRELU_SLOPE)
      xt = c1(xt)
      xt = jax.nn.leaky_relu(xt, LRELU_SLOPE)
      xt = c2(xt)
      x = xt + x
    return x


class ResBlock2(hk.Module):
  def __init__(self, h, channels, kernel_size=3, dilation=(1, 3), name="ResBlock2"):
    super().__init__(name=name)
    self.h = h
    self.convs = [
        hk.Conv1D(channels, kernel_size, 1, rate=dilation[i], padding=get_padding(kernel_size, dilation[i]))
        for i in range(2)
    ]

  def __call__(self, x):
    for c in self.convs:
      xt = jax.nn.leaky_relu(x, LRELU_SLOPE)
      xt = c(xt)
      x = xt + x
    return x


class Generator(hk.Module):
  def __init__(self, h):
    super().__init__()
    self.h = h
    self.num_kernels = len(h.resblock_kernel_sizes)
    self.num_upsamples = len(h.upsample_rates)
    self.conv_pre = hk.Conv1D(h.upsample_initial_channel, 7, 1, padding=((3, 3),))
    resblock = ResBlock1 if h.resblock == '1' else ResBlock2
    self.ups = []
    for i, (u, k) in enumerate(zip(h.upsample_rates, h.upsample_kernel_sizes)):
      self.ups.append(
          hk.Conv1DTranspose(h.upsample_initial_channel//(2**(i+1)), kernel_shape=k,
                             stride=u, padding='SAME', name=f"ups_{i}")
      )

    self.resblocks = []

    for i in range(len(self.ups)):
      ch = h.upsample_initial_channel // (2**(i+1))
      for j, (k, d) in enumerate(zip(h.resblock_kernel_sizes, h.resblock_dilation_sizes)):
        self.resblocks.append(resblock(h, ch, k, d, name=f'res_block1_{len(self.resblocks)}'))
    self.conv_post = hk.Conv1D(1, 7, 1, padding=((3, 3),))

  def __call__(self, x):
    x = self.conv_pre(x)
    for i in range(self.num_upsamples):
      x = jax.nn.leaky_relu(x, LRELU_SLOPE)

      x = self.ups[i](x)
      xs = None
      for j in range(self.num_kernels):
        if xs is None:
          xs = self.resblocks[i*self.num_kernels+j](x)
        else:
          xs += self.resblocks[i*self.num_kernels+j](x)
      x = xs / self.num_kernels
    x = jax.nn.leaky_relu(x)  # default pytorch value
    x = self.conv_post(x)
    x = jnp.tanh(x)
    return x

# import torch
# import torch.nn as nn
# from omegaconf import OmegaConf

# from .lvcnet import LVCBlock

# MAX_WAV_VALUE = 32768.0

# class Generator(nn.Module):
#     """UnivNet Generator"""
#     def __init__(self, hp):
#         super(Generator, self).__init__()
#         self.mel_channel = hp.audio.n_mel_channels
#         self.noise_dim = hp.gen.noise_dim
#         self.hop_length = hp.audio.hop_length
#         channel_size = hp.gen.channel_size
#         kpnet_conv_size = hp.gen.kpnet_conv_size

#         self.res_stack = nn.ModuleList()
#         hop_length = 1
#         for stride in hp.gen.strides:
#             hop_length = stride * hop_length
#             self.res_stack.append(
#                 LVCBlock(
#                     channel_size,
#                     hp.audio.n_mel_channels,
#                     stride=stride,
#                     dilations=hp.gen.dilations,
#                     lReLU_slope=hp.gen.lReLU_slope,
#                     cond_hop_length=hop_length,
#                     kpnet_conv_size=kpnet_conv_size
#                 )
#             )
        
#         self.conv_pre = \
#             nn.utils.weight_norm(nn.Conv1d(hp.gen.noise_dim, channel_size, 7, padding=3, padding_mode='reflect'))

#         self.conv_post = nn.Sequential(
#             nn.LeakyReLU(hp.gen.lReLU_slope),
#             nn.utils.weight_norm(nn.Conv1d(channel_size, 1, 7, padding=3, padding_mode='reflect')),
#             nn.Tanh(),
#         )

#     def forward(self, c, z):
#         '''
#         Args: 
#             c (Tensor): the conditioning sequence of mel-spectrogram (batch, mel_channels, in_length) 
#             z (Tensor): the noise sequence (batch, noise_dim, in_length)
        
#         '''
#         z = self.conv_pre(z)                # (B, c_g, L)

#         for res_block in self.res_stack:
#             res_block.to(z.device)
#             z = res_block(z, c)             # (B, c_g, L * s_0 * ... * s_i)

#         z = self.conv_post(z)               # (B, 1, L * 256)

#         return z

#     def eval(self, inference=False):
#         super(Generator, self).eval()
#         # don't remove weight norm while validation in training loop
#         if inference:
#             self.remove_weight_norm()

#     def remove_weight_norm(self):
#         print('Removing weight norm...')

#         nn.utils.remove_weight_norm(self.conv_pre)

#         for layer in self.conv_post:
#             if len(layer.state_dict()) != 0:
#                 nn.utils.remove_weight_norm(layer)

#         for res_block in self.res_stack:
#             res_block.remove_weight_norm()

#     def inference(self, c, z=None):
#         # pad input mel with zeros to cut artifact
#         # see https://github.com/seungwonpark/melgan/issues/8
#         zero = torch.full((1, self.mel_channel, 10), -11.5129).to(c.device)
#         mel = torch.cat((c, zero), dim=2)
        
#         if z is None:
#             z = torch.randn(1, self.noise_dim, mel.size(2)).to(mel.device)

#         audio = self.forward(mel, z)
#         audio = audio.squeeze() # collapse all dimension except time axis
#         audio = audio[:-(self.hop_length*10)]
#         audio = MAX_WAV_VALUE * audio
#         audio = audio.clamp(min=-MAX_WAV_VALUE, max=MAX_WAV_VALUE-1)
#         audio = audio.short()

#         return audio

# if __name__ == '__main__':
#     hp = OmegaConf.load('../config/default.yaml')
#     model = Generator(hp)

#     c = torch.randn(3, 100, 10)
#     z = torch.randn(3, 64, 10)
#     print(c.shape)

#     y = model(c, z)
#     print(y.shape)
#     assert y.shape == torch.Size([3, 1, 2560])

#     pytorch_total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
#     print(pytorch_total_params)
