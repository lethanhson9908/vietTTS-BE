# # def check_len_text(text):
# #     num_of_char = 500
# #     temp = text
# #     count = 0 
# #     i = 0
# #     split_text = []
# #     while count+num_of_char < len(text):
# #         x = temp[count:count+num_of_char].rindex(".")
# #         split_text.append(temp[count:count+x+1])
# #         #print('------------------------------------')
# #         count = count + x + 1
# #         i +=1
# #     left = temp[count:len(text)]
# #     split_text.append(left)
# #     print(len(split_text))
# #     for text in split_text:
# #         print(text)
# #         print(len(text))
# #         print('--------------')
# #     return split_text

# # # text = 'Trước khi Thế vận hội khai mạc, nhiều nhà khoa học đã cảnh báo Olympic có thể tạo ra các ổ dịch lớn làm lây lan virus ra cộng đồng dân cư nói chung. Đây là rủi ro luôn đi kèm khi tổ chức các sự kiện quốc tế lớn giữa đại dịch. Nhưng thực tế cho thấy, Nhật Bản dường như đã kiểm soát tốt tình hình. Các vận động viên và quan chức thể thao nước ngoài đến Nhật Bản từ tháng trước được yêu cầu xét nghiệm Covid-19 hai lần trong vòng 96 tiếng trước khi chuyến bay của họ khởi hành, tiếp tục xét nghiệm thêm một lần nữa khi tới nơi và cách ly trong ba ngày đầu. Vận động viên phải xét nghiệm hàng ngày trong thời gian ở Nhật Bản và rời đi trong 48 tiếng sau khi môn thi của họ kết thúc. tiếp tục xét nghiệm thêm một lần nữa khi tới nơi và cách ly trong ba ngày đầu. Vận động viên phải xét nghiệm hàng ngày trong thời gian ở Nhật Bản và rời đi trong 48 tiếng sau khi môn thi của họ kết thúc. tiếp tục xét nghiệm thêm một lần nữa khi tới nơi và cách ly trong ba ngày đầu. Vận động viên phải xét nghiệm hàng ngày trong thời gian ở Nhật Bản và rời đi trong 48 tiếng sau khi môn thi của họ kết thúc.'
# # # print(text, len(text))
# # # split_text = check_len_text(text)

# # from pydub import AudioSegment
# # audio_list = ['/home/son/Downloads/hhp/text_to_speech_hhp/output/2021_08_12_15_28_49_0.wav','/home/son/Downloads/hhp/text_to_speech_hhp/output/2021_08_12_15_28_49_1.wav', '/home/son/Downloads/hhp/text_to_speech_hhp/output/2021_08_12_15_28_49_2.wav'] 

# # wavs = [AudioSegment.from_wav(wav) for wav in audio_list]
# # combined = (wavs[0])
# # file_path = '/home/son/Downloads/hhp/text_to_speech_hhp/output/2021_08_12_15_28_49.wav'
# # for wav in wavs[1:]:
# #     combined = combined.append(wav)
# # combined.export(file_path, format="wav", parameters=["-ar", "16000"])
# import torch
# mel_c = torch.randn(1,2,3)
# # print(mel_c)
# # x = mel_c.shape
# # print(x[0],x[1],x[2])
# # mel_y = torch.reshape(mel_c,(1, 3, 2))
# # print(mel_y)
# # zero = torch.full((1, 10, 80), -11.5129)
# # print(zero, zero.shape)
# # mel = torch.cat((mel_c, zero), dim=2)
# # print(mel, mel.shape)

# x = torch.randn(1,2,3)
# print(x)
# y = x.transpose(1,2)
# print(y)
import pickle
import time
start_time = time.time()
ckpt_dir = '/home/son/Downloads/text_to_speech_hhp_final/assets/son/'
with open(ckpt_dir + 'duration_ckpt_latest.pickle', 'rb') as f_d:
  dic_d = pickle.load(f_d)

print("--- duration model: %s seconds ---" % (time.time() - start_time))

start_time = time.time()
with open(ckpt_dir + 'acoustic_ckpt_latest.pickle', 'rb') as f_a:
  dic_a = pickle.load(f_a)

print("--- duration model: %s seconds ---" % (time.time() - start_time))