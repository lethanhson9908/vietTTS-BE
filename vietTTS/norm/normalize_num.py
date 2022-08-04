import string
from vietnam_number import n2w
from vietnam_number import n2w_single
import re
from .normalize_word import *

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

#Số thành từ đầy đủ (có từ nối)
def num_to_words(num):
  #đầu vào là 1 xâu biểu diễn số, ví dụ: 1234
  #chuyển xâu đó về dạng chữ của số, có từ nối
  if num == '':
    return num
  if len(num) > 12:
    return num
  pattern = '[^0-9]'
  match = re.search(pattern, num)
  if not match:
    if num[0] == '0':
      return num
    else:
      a = n2w(num)
      a = a.split()
      for i in range(len(a)):
        if a[i] == 'lẽ':
          a[i] = 'lẻ'
      last = len(a) - 1
      if a[last-1] + a[last] == 'khôngtrăm':
        a = a[:-2]
        last -= 2
        while last >= 2 and a[last-2] + a[last-1] == 'khôngtrăm':
          a = a[:-3]
          last -= 3
      a = ' '.join(a)
      return a
  else:
    return num

#Số thành từ không có từ nối
def num_to_words_single(num):
  if num == '':
    return num
  pattern = '[^0-9]'
  match = re.search(pattern, num)
  if not match:
    b = n2w_single(num)
    return b
  else:
    return num

#Số có dấu , và . ở giữa
def num_punc_to_words(num):
  if num == '':
    return num
  char = '0123456789,.'
  for l in num:
    if l not in char:
      return num
  last = len(num) - 1
  if num[last] == ',' or num[last] == '.':
    return num
  if last == 0:
    return num
  if num[0] == '0' and (num[1] == '.' or num[1] == ','):
    num = 'không phảy ' + num_to_words_single(num[2:])
  else:
    if '.' in num:
      re_punc = re.compile('[%s]' % re.escape('.'))
      num = re_punc.sub('', num)
      if num[0] == '0':
        num = num_to_words_single(num)
      else:
        num = num_to_words(num)
        num = num_to_words_single(num)
      return num
    elif ',' in num:
      l = num.split(',')
      text = num_to_words(l[0]) + ' phảy ' + num_to_words_single(l[1])
      return text
  return num

#Số đi với đơn vị 
def num_unit_to_words(num, unit_list):
  if num == '':
    return num
  n = '0123456789,.'
  last = len(num) - 1
  k = 0
  for i in range(len(num)):
    if not num[i] in n:
      k = i
      break
  if k > 0:
    if (k < last and num[k+1] not in n):
      unit = num[k:]
      num = num[:k]
      num = num_to_words(num)
      num = num_to_words_single(num)
      num = num_punc_to_words(num)
      unit = unit_di_unit(unit, unit_list).split()
      for i in range(len(unit)):
        if unit[i] in unit_list:
          unit[i] = unit_list[unit[i]]
      unit = ' '.join(unit)
      words = num + ' ' + unit
      return words
    elif k == last:
      unit = num[k:]
      num = num[:k]
      num = num_to_words(num)
      num = num_to_words_single(num)
      num = num_punc_to_words(num)
      unit = unit_di_unit(unit, unit_list).split()
      for i in range(len(unit)):
        if unit[i] in unit_list:
          unit[i] = unit_list[unit[i]]
      unit = ' '.join(unit)
      words = num + ' ' + unit
      return words
    else:
      return num
  else:
    return num

#Từ số này đến số kia 1-2
def from_n2n_words(num, unit_list):
  if num == '':
    return num
  if '-' not in num:
    return num
  else:
    l = num.split('-')
    n_from = l[0]
    n_to = l[1]
    
    n_from = num_to_words(n_from)
    n_from = num_to_words_single(n_from)
    n_from = num_punc_to_words(n_from)
    n_from = num_unit_to_words(n_from, unit_list)
    n_to = num_to_words(n_to)
    n_to = num_to_words_single(n_to)
    n_to = num_punc_to_words(n_to)
    n_to = num_unit_to_words(n_to, unit_list)
    
    words = n_from + ' đến ' + n_to
    return words
