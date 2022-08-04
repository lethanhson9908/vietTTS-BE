import os
import glob
import tqdm
import torch
import argparse
from scipy.io.wavfile import write
from omegaconf import OmegaConf

from univnet.model.generator import Generator


def mel2wave_univ(mel, checkpoint_path):
    checkpoint = torch.load(checkpoint_path)
    #   if args.config is not None:
    #     hp = OmegaConf.load(args.config)
    #   else:
    hp = OmegaConf.create(checkpoint['hp_str'])
    #model = Generator(hp).cuda()
    model = Generator(hp)
    saved_state_dict = checkpoint['model_g']
    new_state_dict = {}

    for k, v in saved_state_dict.items():
        try:
            new_state_dict[k] = saved_state_dict['module.' + k]
        except:
            new_state_dict[k] = v
    model.load_state_dict(new_state_dict)
    model.eval(inference=True)
    if len(mel.shape) == 2:
        mel = mel.unsqueeze(0)
    mel_c = mel.transpose(1,2)
    #print(len(mel_c.shape), mel_c.shape)
    #mel = mel.cuda()

    audio = model.inference(mel_c)
    audio = audio.cpu().detach().numpy()
    return audio

