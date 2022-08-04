from .normalize_word import *
from .normalize_num import *
from .normalize_time import *
import argparse

unit_list = {
    'mm': 'mi li mét',
    'cm': 'xăng ti mét',
    'dm': 'đề xi mét',
    'm': 'mét',
    'dam': 'đề ca mét',
    'hm': 'héc tô mét',
    'km': 'ki lô mét',
    'mm2': 'mi li mét vuông',
    'cm2':'xăng ti mét vuông',
    'm2': 'mét vuông',
    'km2': 'ki lô mét vuông',
    'mm3': 'mi li mét khối',
    'cm3': 'xăng ti mét khối',
    'm3': 'mét khối',
    'km3': 'ki lô mét khối',
    'ml' : 'mi li lít',
    'l': 'lít',
    'g': 'gam',
    'mg': 'mi li gam',
    'kg': 'ki lô gam',
    '%' : 'phần trăm',
    '$' : 'đô la',
    'oC': 'độ xê',
    's' : 'giây',
    'ms': 'mi li giây',
    'h' : 'giờ',
    'p' : 'phút',
    'px': 'pít xeo'
}

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", default=None, type=str, required=True, help="input file")
parser.add_argument("--output_file", default=None, type=str, required=True, help="input file")
args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file

file_object = open(output_file, 'a+', encoding='utf-8')
k = 0
number = '[0-9]'
with open(input_file, 'r', encoding="utf-8") as f:
  while True:
    k += 1
    sen = f.readline()
    if not sen:
      break
    sen = sen.lower().strip()
    list_word = sen.split()
    for i in range(len(list_word)):
    #print(list_word[i])
      list_word[i] = rm_punc_word(list_word[i])
      if list_word[i] == '':
        continue
      if list_word[i-1] in ['từ', 'khoảng'] and '-' in list_word[i]:
        list_word[i] = from_n2n_words(list_word[i], unit_list)
        continue
      list_word[i] = num_to_words(list_word[i])
      list_word[i] = num_to_words_single(list_word[i])
      
      list_word[i] = full_date_to_words(list_word[i])
      if list_word[i-1] in ['ngày','hôm','qua','kia','sáng','chiều','tối','hai','ba','tư','năm','sáu','bảy','nhật']:
        pre_word = list_word[i]
        list_word[i] = date_to_words(list_word[i])
        if list_word[i] != pre_word:
          continue
      if list_word[i-1] == 'tháng':
        pre_word = list_word[i]
        list_word[i] = month_to_words(list_word[i])
        if list_word[i] != pre_word:
          continue
    
      list_word[i] = num_punc_to_words(list_word[i])
      list_word[i] = num_unit_to_words(list_word[i], unit_list)
      list_word[i] = time_to_words(list_word[i])
      list_word[i] = unit_to_word(list_word[i], unit_list)
      list_word[i] = unit_di_unit(list_word[i], unit_list)
    list_word = ' '.join(list_word).strip()
    if re.search(number, list_word):
      continue
    else:
      re_punc = re.compile('[%s]' % re.escape(string.punctuation))
      list_word = re_punc.sub(' ', list_word)
      words = list_word.split()
      for i in range(len(words)):
        words[i] = words[i].strip()
      list_word = ' '.join(words).strip()
      if list_word == '':
        continue

      file_object.write(list_word + '\n')
    print(k)

file_object.close()


