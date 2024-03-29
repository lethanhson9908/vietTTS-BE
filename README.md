A Vietnamese TTS
================
This repo is based on: https://github.com/NTT123/vietTTS

I replace HifiGAN vocoder by UnivNet vocoder and keep Tacotron2 for vietnamese datasets. I also deploy simple API using FastAPI in main.

A synthesized audio clip: [clip.wav](assets/infore/clip.wav). A colab notebook: [notebook](https://colab.research.google.com/drive/1oczrWOQOr1Y_qLdgis1twSlNZlfPVXoY?usp=sharing).

*Chú ý các cài đặt phía dưới là mặc định có các file weights, trong trường hợp chưa có, ta có thể tải tại đây:
https://drive.google.com/drive/folders/1yS8tdPC84VCAJqvgA5ienC8G6SJpghPV?usp=sharing

Cài đặt
-------
Nếu máy chưa cài ffmpeg :
```sh
sudo apt install ffmpeg
```

```sh
#git clone https://github.com/NTT123/vietTTS.git
cd root_directory (thư mục gốc clone về)
pip3 install -r requirements.txt
cd vietTTS 
pip3 install -e .

```
Để chạy app
----------------------------------
```
cd to root directory (text_to_speech_hhp)
uvicorn main:app --reload
```
all config in main.py

Quick start sử dụng pretrained models
----------------------------------
```sh
bash ./scripts/quick_start.sh
```


Tải InfoRe dataset
-----------------------

```sh
bash ./scripts/download_aligned_infore_dataset.sh
```


The Montreal Forced Aligner (MFA) được sử dụng để căn chỉnh textGrid và audio (textgrid files). [Here](https://colab.research.google.com/gist/NTT123/c99b5a391af56e0cb8f7b190d3d7f0ee/infore-mfa-example.ipynb) is a Colab notebook to align InfoRe dataset. Visit [MFA](https://montreal-forced-aligner.readthedocs.io/en/latest/) for more information on how to create textgrid files.

Train duration model
--------------------

```sh
python3 -m vietTTS.nat.duration_trainer
```


Train acoustic model
--------------------
```sh
python3 -m vietTTS.nat.acoustic_trainer
```



Train UnivNet vocoder
-------------

HiFiGAN vocoder implement from  https://github.com/mindslab-ai/univnet . Read their README to train vocoder

```sh
git clone https://github.com/mindslab-ai/univnet

├── assets                                #Nơi chứa các file weight 
│   ├── hifigan
│   │   └── config.json
│   ├── infore
│   │   ├── hifigan
│   │   │   ├── g_01330000                #file weight HifiGAN (chuyển từ mel spectrogram -> audio)
│   │   │   └── hk_hifi.pickle
│   │   ├── lexicon.txt                   #file từ điển dùng cho train model
│   │   └── nat
│   ├── son
│   │   ├── acoustic_ckpt_latest.pickle  #file weight acoustic model (chuyen tu text -> mel spectrogram)
│   │   └── duration_ckpt_latest.pickle  #file weight duration model (chỉnh tốc độ ngắt nghỉ như dữ liệu training)
│   ├── transcript
│   │   └── preprocess
│   └── transcript.txt
├── dict.txt                              #file từ điển thay thế khi không biểu diễn từ đó được ( VD: 1 -> một, 2-> hai,...)
├── download_weight.py
├── hifi-gan                              #Thư mục dùng để train HifiGAN (mel spectrogram -> audio)
│   ├── config.json                       #file config custom training 
│   ├── config_v1.json
│   ├── config_v2.json
│   ├── config_v3.json
│   ├── data.html
│   ├── env.py
│   ├── files.txt
│   ├── inference_e2e.py
│   ├── inference.py
│   ├── LICENSE
│   ├── LJSpeech-1.1
│   │   ├── training.txt
│   │   └── validation.txt
│   ├── meldataset.py
│   ├── models.py
│   ├── __pycache__
│   │   ├── env.cpython-37.pyc
│   │   ├── meldataset.cpython-37.pyc
│   │   ├── models.cpython-37.pyc
│   │   └── utils.cpython-37.pyc
│   ├── README.md
│   ├── requirements.txt
│   ├── train_files.txt                   # luu danh sach file training
│   ├── train.py
│   ├── utils.py
│   ├── val_files.txt
│   └── validation_loss.png               #luu danh sach file val
├── LICENSE
├── main.py                               #file viết API 
├── output                                #thư mục audio đầu ra sau khi truyền text vào (có thể custom)
│   ├── 2021_08_12_15_54_27_0.wav         #format: YYYY_mm_dd_hh_MM_ss_{part_x} (part_x trong trường hợp text đầu vào quá dài thì cắt nhỏ)
│   ├── 2021_08_12_15_54_27_1.wav
│   ├── 2021_08_12_15_54_27.wav
│   ├── 2021_08_12_16_23_35_0.wav
│   ├── 2021_08_12_16_23_35.wav
├── __pycache__
│   └── main.cpython-38.pyc
├── README.md
├── requirements.txt                      #chứa các thư viện đi kèm
├── scripts
│   ├── download_aligned_infore_dataset.sh
│   └── quick_start.sh
├── setup.cfg
├── setup.py
├── test.py
├── tests
│   ├── test_nat_acoustic.py
│   └── test_nat_duration.py
├── vietTTS                                  
│   ├── hifigan                             #thư mục dùng để chuyển từ mel -> audio khi inference 
│   │   ├── config.py
│   │   ├── convert_torch_model_to_haiku.py #chuyển sang haiku để tối ưu tốc độ convert từ mel-> audio
│   │   ├── create_mel.py
│   │   ├── data_loader.py
│   │   ├── mel2wave.py
│   │   ├── model.py
│   │   ├── torch_model.py
│   │   └── trainer.py
│   ├── __init__.py
│   ├── nat                                  #Thư mục dùng để train acoustic và duration model
│   │   ├── acoustic_trainer.py
│   │   ├── config.py
│   │   ├── data_loader.py
│   │   ├── dsp.py
│   │   ├── duration_trainer.py
│   │   ├── gta.py
│   │   ├── __init__.py
│   │   ├── model.py
│   │   ├── text2mel.py
│   │   ├── utils.py
│   │   └── zero_silence_segments.py
│   ├── __pycache__
│   │   ├── __init__.cpython-37.pyc
│   │   ├── __init__.cpython-38.pyc
│   │   ├── main.cpython-38.pyc
│   │   ├── synthesizer.cpython-37.pyc
│   │   └── synthesizer.cpython-38.pyc
│   └── synthesizer.py                    #file chuyển từ text -> audio ( file quan trọng nhất)
└── vietTTS.egg-info
    ├── dependency_links.txt
    ├── PKG-INFO
    ├── requires.txt
    ├── SOURCES.txt
    └── top_level.txt

