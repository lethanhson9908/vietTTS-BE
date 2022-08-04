import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
#from vietTTS.synthesizer import * 
from starlette.responses import RedirectResponse
from pydantic import BaseModel
import re
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
from pydub import AudioSegment
import base64
from vietTTS.synthesizer import *

dir = '/home/haunt32/ai-bigdata/TTS/'

APP_DESC = "text-to-speech HHP"

app = FastAPI(title='Text to speech Demo', description=APP_DESC)

# origins = [
#     "http://0.0.0.0:3000",
#     "http://192.168.0.109:5000",
#     "http://10.38.23.47:3000",
#     "http://api-tts.mbfbigdata.vn/TTS"
# ]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")

class TTSRequest(BaseModel):
    text: str
    #model: str
class TTSResponse(BaseModel):
    audio_path : str
    text : str

def check_len_text(text):
    num_of_char = 2000
    temp = text
    count = 0 
    i = 0
    split_text = []
    while count+num_of_char < len(text):
        x = temp[count:count+num_of_char].rindex(".")
        split_text.append(temp[count:count+x+1])
        #print('------------------------------------')
        count = count + x + 1
        i +=1
    left = temp[count:len(text)]
    split_text.append(left)
    
    return split_text

@app.post("/TTS", response_model = TTSResponse)
def TTS(request: TTSRequest):
    text = request.text
    #print('preprocess text...')
    # text = change_text(request.text)
    split_text = check_len_text(text)
    counter = 0
    audio_list = []
    now = datetime.now()
    date_time = now.strftime("%Y_%m_%d_%H_%M_%S_")
    for text in split_text:
        print(text, len(text))
        print('-------------')
        audio_output = dir + 'output/'+date_time+str(counter)+'.wav'
        # os.system(f'python3 -m vietTTS.synthesizer --text "{text}" --output "{audio_output}" --lexicon-file assets/infore/lexicon.txt --silence-duration 0.20')
        synthesise(text, output=audio_output)
        counter += 1
        audio_list.append(audio_output)
    wavs = [AudioSegment.from_wav(wav) for wav in audio_list]
    combined = (wavs[0])
    file_path = audio_list[0][:-6] +'.wav'
    
    for wav in wavs[1:]:
        combined = combined.append(wav)
    combined.export(file_path, format="wav", parameters=["-ar", "16000"])
    print(audio_list)
    with open(file_path, "rb") as audio_file:
        res_64 = (base64.b64encode(audio_file.read())).decode('ascii')
        print(type(res_64))
    return  TTSResponse(audio_path = res_64, text = text)

if __name__ == "__main__":
    uvicorn.run(app, port = 8000, host='0.0.0.0')
#uvicorn main:app --reload