import string
from vietnam_number import n2w
from vietnam_number import n2w_single
import re
from .normalize_word import *
from .normalize_num import *

#Ngày đầy đủ thành từ
def full_date_to_words(date):
  #chuyển đổi ngày/thang và ngày/tháng/năm sang chữ
  date = date.strip()
  if date == '':
    return date
  patternfull1 = '(\d{1,2})[/](\d{1,2})[/](\d{3,4})'
  patternfull2 = '(\d{1,2})[.](\d{1,2})[.](\d{3,4})'
  patternfull3 = '(\d{1,2})[-](\d{1,2})[-](\d{3,4})'

  matchfull1 = re.match(patternfull1, date)
  matchfull2 = re.match(patternfull2, date)
  matchfull3 = re.match(patternfull3, date)
  matchfull = [matchfull1, matchfull2, matchfull3]
  k = 0
  for i in date:
    if i == '.':
      k+=1
  if k>= 3:
    return date
  k = 0
  for i in date:
    if i == '/':
      k+=1
  if k>= 3:
    return date
  k = 0
  for i in date:
    if i == '-':
      k+=1
  if k>= 3:
    return date
  for m in matchfull:
    if m:
      l = list(m.groups())
      for i in range(len(l)):
        if l[i][0] == '0':
          l[i] = l[i][1:]
        l[i] = num_to_words(l[i])
      l = tuple(l)
      strdate = '{} tháng {} năm {}'.format(*l)
      return strdate
  return date

#Ngày tháng thành từ
def date_to_words(date):
  date = date.strip()
  if date == '':
    return date
  pattern1 = '(\d{1,2})[/](\d{1,2})'
  pattern2 = '(\d{1,2})[.](\d{1,2})'
  pattern3 = '(\d{1,2})[-](\d{1,2})'

  match1 = re.match(pattern1, date)
  match2 = re.match(pattern2, date)
  match3 = re.match(pattern3, date)
  match = [match1, match2, match3]
  k = 0
  for i in date:
    if i == '.':
      k+=1
  if k>= 2:
    return date
  k = 0
  for i in date:
    if i == '/':
      k+=1
  if k>= 2:
    return date
  k = 0
  for i in date:
    if i == '-':
      k+=1
  if k>= 2:
    return date
  for m in match:
    if m:
      l = list(m.groups())
      for i in range(len(l)):
        if l[i][0] == '0':
          l[i] = l[i][1:]
        l[i] = num_to_words(l[i])
      l = tuple(l)
      strdate = '{} tháng {}'.format(*l)
      return strdate
  return date

#Năm tháng thành từ
def month_to_words(month):
  #chuyển đổi tháng/năm sang chữ
  month = month.strip()
  if month == '':
    return month
  pattern1 = '(\d{1,2})[/](\d{3,4})'
  pattern2 = '(\d{1,2})[-](\d{3,4})'
  pattern3 = '(\d{1,2})[.](\d{3,4})'

  match1 = re.match(pattern1, month)
  match2 = re.match(pattern2, month)
  match3 = re.match(pattern3, month)
  match = [match1, match2, match3]
  for m in match:
    if m:
      l = list(m.groups())
      for i in range(len(l)):
        if l[i][0] == '0':
          l[i] = l[i][1:]
        l[i] = num_to_words(l[i])
      l = tuple(l)
      strdate = '{} năm {}'.format(*l)
      return strdate
  return month

#Giờ phút thành từ
def time_to_words(time):
  time = time.strip()
  if time == '':
    return time

  num = '[0-9]'
  c = '0123456789h:p'
  if not re.search(num, time):
    return time

  for i in range(len(time)):
    if time[i] not in c:
      return time

  pattern1 = '(\d{1,2})[h](\d{1,2})'
  pattern2 = '(\d{1,2})[:](\d{1,2})'
  pattern3 = '(\d{1,2})[h](\d{1,2})[p]'
  pattern4 = '(\d{1,2})[:](\d{1,2})[p]'
  match1 = re.match(pattern1, time)
  match2 = re.match(pattern2, time)
  match3 = re.match(pattern3, time)
  match4 = re.match(pattern4, time)
  
  if match1 and time[-1] in c[:-3]:
    time = time.split('h')
    hour = num_to_words(time[0])
    hour = num_to_words_single(hour)
    min = num_to_words(time[1])
    min = num_to_words_single(min)
    words = hour + ' giờ ' + min + ' phút'
    return words
  elif match2 and time[-1] in c[:-3]:
    time = time.split(':')
    hour = num_to_words(time[0])
    hour = num_to_words_single(hour)
    min = num_to_words(time[1])
    min = num_to_words_single(min)
    words = hour + ' giờ ' + min + ' phút'
    return words
  elif match3 and time[-1] == 'p':
    time = time[:-1]
    time = time.split('h')
    hour = num_to_words(time[0])
    hour = num_to_words_single(hour)
    min = num_to_words(time[1])
    min = num_to_words_single(min)
    words = hour + ' giờ ' + min + ' phút'
    return words
  elif match4 and time[-1] == 'p':
    time = time[:-1]
    time = time.split(':')
    hour = num_to_words(time[0])
    hour = num_to_words_single(hour)
    min = num_to_words(time[1])
    min = num_to_words_single(min)
    words = hour + ' giờ ' + min + ' phút'
    return words
  else:
    return time
