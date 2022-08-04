import re
import unicodedata
from argparse import ArgumentParser
from pathlib import Path
import jax
import torch
import soundfile as sf
import os
from .hifigan.mel2wave import mel2wave
from .hifigan.mel2wav_univ import mel2wave_univ
from .nat.config import FLAGS
from .nat.text2mel import text2mel
from .norm.tts_norm import *
import time

parser = ArgumentParser()
parser.add_argument('--text', type=str)
parser.add_argument('--output', default='clip.wav', type=Path)
parser.add_argument('--sample-rate', default=16000, type=int)
parser.add_argument('--silence-duration', default=-1, type=float)
parser.add_argument('--lexicon-file', default=None)
args = parser.parse_args()
checkpoint_path = './assets/infore/hifigan/g_1015.pt'

def nat_normalize_text(text):
  text = unicodedata.normalize('NFKC', text)
  text = preprocess_text(text)
  text = text.lower().strip()
  sp = FLAGS.special_phonemes[FLAGS.sp_index]
  text = re.sub(r'[\n.,:]+', f' {sp} ', text)
  text = text.replace('"', " ")
  text = re.sub(r'\s+', ' ', text)
  text = re.sub(r'[.,:;?!]+', f' {sp} ', text)
  text = re.sub('[ ]+', ' ', text)
  text = re.sub(f'( {sp}+)+ ', f' {sp} ', text)
  text = norm_text(text)
  text = text.replace('vê ê', 'vê')
  return text.strip()

def synthesise(text, output,lexicon_file='assets/infore/lexicon.txt', silence_duration=0.20, sample_rate=16000):
  text = nat_normalize_text(text)
  print('Normalized text input:', text)
  mel = text2mel(text, lexicon_file, silence_duration)
  mel_device = jax.device_get(mel)
  mel_torch = torch.from_numpy(mel_device)

  # start_time = time.time()
  # wave = mel2wave(mel)
  # print("--- hifigan: %s seconds ---" % (time.time() - start_time))

  univ_start_time = time.time()
  wave_univ = mel2wave_univ(mel_torch, checkpoint_path=checkpoint_path)
  print("--- univnet: %s seconds ---" % (time.time() - univ_start_time))

  # print('writing output to file', output)
  # sf.write(str(output), wave, samplerate=sample_rate)
  univ_output = str(output)
  sf.write(univ_output, wave_univ, samplerate=sample_rate)
  