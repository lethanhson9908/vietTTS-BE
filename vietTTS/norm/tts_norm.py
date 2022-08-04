import string
import re
from .normalize_word import *
from .normalize_num import *
from .normalize_time import *
import argparse

pattern_upper = '([A-Z]+[A-Z]+)'

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

char_list = {
    "V" : "Vê ",
    "A": "A",
    "B": "Bê",
    "C": "Xê",
    "D": "Dê",
    "Đ": "Đê",
    "E": "E",
    "Ê": "Ê",
    "F": "Ép",
    "G": "Gờ",
    "H": "Hát",
    "I": "Y",
    "J": "Di",
    "K": "Ca",
    "L": "Lờ",
    "M": "Mờ",
    "N": "Nờ",
    "O": "O",
    "Ô": "Ô",
    "Ơ" : "Ơ",
    "P" : "Pê",
    "Q" : "Qui",
    "R" : "Rờ",
    "S" : "Ét",
    "T" : "Tê",
    "U" : "U",
    "Ư" : "Ư",
    "W" : "Vê kép",
    "X" : "ích",
    "Y" : "Y",
    "Z" : "dét"
}

def preprocess_text(text, remove_special_character=False):
    converted = text
    replace_chars = list(string.punctuation.replace("'", "").replace("-", "").replace("\n"," "))
    if remove_special_character:
        for char in replace_chars:
            text = text.replace(char, " ")
    else:
        for char in replace_chars:
            text = text.replace(char, " " + char +" ")
    res = re.findall(pattern_upper, text)
    for word in res:
        old_word = word
        for char in word:
            for key in char_list.keys():
                if key == char:
                    word = word.replace(char, char_list[key]+ ' ')
        converted = re.sub(old_word, word, converted)
        print(old_word, word)
    return " ".join(converted.split())

def norm_text(preprocessed_text):
    number = '[0-9]'
    preprocessed_text = preprocessed_text.lower().strip()
    list_word = preprocessed_text.split()

    for i in range(len(list_word)):
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
        pass
    else:
        re_punc = re.compile('[%s]' % re.escape(string.punctuation))
        list_word = re_punc.sub(' ', list_word)
        words = list_word.split()
        for i in range(len(words)):
            words[i] = words[i].strip()
        list_word = ' '.join(words).strip()
        if list_word == '':
            pass
    return list_word

