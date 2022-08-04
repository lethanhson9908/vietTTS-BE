import string
from vietnam_number import n2w
from vietnam_number import n2w_single
import re

#Bỏ dấu đầu và cuối từ
def rm_punc_word(word):
  punctuation = string.punctuation.replace('%', '')
  punctuation = punctuation.replace('$', '')
  word = word.strip()
  if word == '':
    return word
  k=0
  for l in word:
    if l not in punctuation:
      k += 1
  if k == 0:
    return ''
  last = len(word) - 1
  while word[0] in punctuation:
    word = word[1:]
    last -= 1
  while word[last] in punctuation:
    word = word[:-1]
    last -=1
  return word

#Chuyển đơn vị thành từ
def unit_to_word(unit, unit_list):
  unit = unit.strip()
  if unit == '':
    return unit
  if unit in unit_list:
    word = unit_list[unit]
    return word
  else:
    return unit

#Chuyển đơn vị/đơn vị thành từ
def unit_di_unit(word, unit_list):
  word = word.strip()
  if word == '':
    return word
  if '/' in word:
    word = word.split('/')
    if word[0] in  unit_list:
      word[0] = unit_list[word[0]]
    if word[1] in  unit_list:
      word[1] = unit_list[word[1]]
    word = word[0] + ' trên ' + word[1]
    return word
  else:
    return word

#Xóa dấu ở giữa từ (không dùng nữa)
def remove_mid_punc(word):
  number = '[0-9]'
  word = word.strip()
  if word == '':
    return word
  if re.search(number, word):
    return word
  word = list(word)
  punc = string.punctuation
  for i in range(len(word)):
    if word[i] in punc:
      word[i] = ' '
  word = ''.join(word)
  return word

'''
#Chuẩn hóa y,i
def normalize_i_y(word):
  #chuẩn hóa âm i và y trong 1 từ
  
  word = word.strip()
  if word == '':
    return word
  last = len(word) - 1
  
  consonants = [ 'b', 'c', 'd', 'đ', 'g', 'h', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'x',
                'B', 'C', 'D', 'Đ', 'G', 'H', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'X']
  l = list(word)
  i_seq = 'iíìịỉĩIÍÌỊỈĨ'
  y_seq = 'yýỳỵỷỹYÝỲỴỶỸ'

  #tạo từ điểm thứ tự các từ i và y
  i_dict_num = {}
  i_dict_let = {}
  y_dict_num = {}
  y_dict_let = {}
  k = 0
  for i in i_seq:
    i_dict_num[k] = i
    i_dict_let[i] = k
    k+=1
  k = 0
  for i in y_seq:
    y_dict_num[k] = i
    y_dict_let[i] = k
    k+=1

  #trường hợp 1 âm tiết
  if len(word) == 1:
    return word
  
  #từ ỉa thì giữ nguyên
  if word == 'ỉa' or word == 'Ỉa':
    return word

  #nếu từ bắt đầu bằng i mà đằng sau là nguyên âm
  if(l[0] in i_seq and not l[1] in consonants):
    l[0] = y_dict_num[i_dict_let[l[0]]]
    word = ''.join(l)
    word = word 
    return word

  #nếu từ bắt đầu bằng y mà đằng sau là phụ âm
  if(l[0] in y_seq and l[1] in consonants):
    l[0] = i_dict_num[y_dict_let[l[0]]]
    word = ''.join(l)
    word = word 
    return word

  #nếu từ kết thúc là y mà trước đó là phụ âm
  if(l[last] in y_seq):
    if(l[last-1] in consonants):
      l[last] = i_dict_num[y_dict_let[l[last]]]
      word = ''.join(l)
      word = word 
      return word

  return word 
'''

def normalize_i_y(word):
  #chuẩn hóa âm i và y trong 1 từ
  
  word = word.strip()
  if word == '':
    return word
  
  if len(word) == 1:
    return word

  last = len(word) - 1
  consonants = [ 'b', 'c', 'd', 'đ', 'g', 'h', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'x',
                'B', 'C', 'D', 'Đ', 'G', 'H', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'X']
  l = list(word)
  i_seq = 'iíìịỉĩIÍÌỊỈĨ'
  y_seq = 'yýỳỵỷỹYÝỲỴỶỸ'

  #tạo từ điểm thứ tự các từ i và y
  i_dict_num = {}
  i_dict_let = {}
  y_dict_num = {}
  y_dict_let = {}
  k = 0
  for i in i_seq:
    i_dict_num[k] = i
    i_dict_let[i] = k
    k+=1
  k = 0
  for i in y_seq:
    y_dict_num[k] = i
    y_dict_let[i] = k
    k+=1

  #nếu từ kết thúc là y mà trước đó là phụ âm
  if(l[last] in y_seq):
    if(l[last-1] in consonants):
      l[last] = i_dict_num[y_dict_let[l[last]]]
      word = ''.join(l) 
      return word

  return word 
