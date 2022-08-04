python3 -m vietTTS.hifigan.convert_torch_model_to_haiku --config-file=assets/hifigan/config.json --checkpoint-file=assets/infore/hifigan/g_01330000
echo "Generate audio clip"
text=`cat assets/transcript.txt`
python3 -m vietTTS.synthesizer --text "$text" --output assets/infore/ok_clip.wav --lexicon-file assets/infore/lexicon.txt --silence-duration 0.20
