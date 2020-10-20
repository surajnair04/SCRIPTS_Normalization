'''
Updated on October 20th, 2020
Version 3.0

@author: reskander
'''
# coding=utf-8

import sys
import re
import unicodedata

punctuation_symbol = '[\_\\"\“\”\‘\’\``\′\՛\.\·\.\ㆍ\•\۔\٫\,\、\;\:\?\？\!\[\]\{\}\(\)\|\«\»\…\،\٬\؛\؟\¿\፤\፣\።\፨\፠\፧\፦\፡\…\।\¡\「\」\《\》\』\『\〔\〕\\\–\—\−\„\‚\´\〉\〈\【\】\（\）\~\。\○\．\♪\‹\<\>\*\/\+\-\=\≠\%\$\£\€\¥\۩\#\°\@\٪\≤\≥\^\φ\θ\×\✓\✔\△\©\☺\♥\❤\❤️\💕\💋\😍\😂\😉\😊\😔\👍\😘\😁\🤔\😃\😄\🙈\😱\☝\🙏\👏]'

digit = '[0123456789٠١۲٢٣٤٥٦٧٨٩۰۴۵۶౦౧౨౩౪౫౬౭౮౯፲፳፴፵፶፷፸፹፺፻०१२३४५६७८९४零一二三四五六七八九十百千万億兆つ]'

number = '^\%?'+digit+'+(([\.\,\:\-\/\٫])?'+digit+')*$'

extras = "[\u200c\u0640\u200e\u200f\u200b\ufeff\u200a\u202b\u200d\u2009\ufe0f]"

english_alphabet = "abcdefghijklmnopqrstuvwxyz"
english_vowels = "aeiou"

swahili_alphabet = "abcdefghijklmnopqrstuvwxyz"
swahili_vowels = "aeiou"

tagalog_alphabet = "abcdefghijklmnopqrstuvwxyz"
tagalog_vowels = "aeiou"

somali_alphabet = "abcdefghijklmnopqrstuvwxyz'"
somali_vowels = "aeiou"

lithuanian_alphabet = "aąbcčdeęėfghiįyjklmnoprsštuųūvzž"
lithuanian_vowels = "aąeęėiįouųū"

bulgarian_alphabet = "абвгдежзийклмнопрстуфхцчшщъьюяѫѣ"
bulgarian_romanized_alphabet = "ŭĭu̐abcdefghijklmnopqrstuvwxyzабвгдежзийклмнопрстуфхцчшщъьюяѫѣ"
bulgarian_vowels = "аеиоуъ"

pashto_diac = "\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652\u0656\u065d\u0670\u0618\u0619\u061A"
pashto_alphabet = "ایردنهموتبسلشکزفگعخقيجحپصآطچضكظغذئثژأىءؤۀةھإ" + pashto_diac
pashto_romanized_alphabet = "abcdefghijklmnopqrstuvwxyz'"+ pashto_alphabet
pashto_vowels = "اويےﮮۍیىې"

farsi_diac = "\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652\u0656\u065d\u0670\u0618\u0619\u061A"
farsi_alphabet = "ایردنهموتبسلشکزفگعخقيجحپصآطچضكظغذئثژأىءؤۀةھإ" + farsi_diac
farsi_romanized_alphabet = "abcdefghijklmnopqrstuvwxyz'" + farsi_alphabet
farsi_vowels = "اویۍۅۆېيىﯼﺎﺍﻮﻭﻰﻳﻴﻲﻱﯽﯾﯿےﮯ"

alphabet_map = {}
alphabet_map["ENG"] = english_alphabet;
alphabet_map["TGL"] = tagalog_alphabet;
alphabet_map["SWA"] = swahili_alphabet;
alphabet_map["SOM"] = somali_alphabet;
alphabet_map["LIT"] = lithuanian_alphabet;
alphabet_map["BUL"] = bulgarian_alphabet;
alphabet_map["BUL_ROM"] = bulgarian_romanized_alphabet;
alphabet_map["PUS"] = pashto_alphabet;
alphabet_map["PUS_ROM"] = pashto_romanized_alphabet;
alphabet_map["FAS"] = farsi_alphabet;
alphabet_map["FAS_ROM"] = farsi_romanized_alphabet;

vowels_map = {}
vowels_map["ENG"] = english_vowels;
vowels_map["TGL"] = tagalog_vowels;
vowels_map["SWA"] = swahili_vowels;
vowels_map["SOM"] = somali_vowels;
vowels_map["LIT"] = lithuanian_vowels;
vowels_map["BUL"] = bulgarian_vowels;
vowels_map["PUS"] = pashto_vowels;
vowels_map["FAS"] = farsi_vowels;

''' Special cases not handled by the default unicode undiacritization '''
latin_character_mappings = {
    'ą': 'a',
    'č': 'c',
    'ę': 'e',
    'ė': 'e',
    'į': 'i',
    'š': 's',
    'ų': 'u',
    'ū': 'u',
    'ž': 'z',
}

''' Special transformation for Pashto '''
pashto_character_mappings = {
    'ق': 'ک',
    'ف': 'پ',
    'ك': 'ک',
    'گ': 'ګ',
    'ﺉ': 'ي',
    'ئ': 'ي',
    'ہ': 'ه',
    'ھ': 'ه',
    'ٸ': 'ي',
    'ؤ': 'و',
    'ﻻ': 'لا',
    'ۓ': 'ي',
    'ے': 'ي',
    'ﮮ': 'ي',
    'ۍ': 'ي',
    'ی': 'ي',
    'ى': 'ي',
    'ې': 'ي',
    'إ': 'ا',
    'آ': 'ا',
    'أ': 'ا',
    'ة': 'ه',
    'ۀ': 'ه',
    #numbers
    '٤': '۴',
    '٥': '۵',
    '٦': '۶',
    '0': '۰',
    '1': '۱',
    '2': '۲',
    '3': '۳',
    '4': '۴',
    '5': '۵',
    '6': '۶',
    '7': '۷',
    '8': '۸',
    '9': '۹'
}

farsi_character_mappings = {
    "آ": "ا",
    "أ": "ا",
    "إ": "ا",
    "ئ": "ی",
    "ى": "ی",
    "ي": "ی",
    "ؤ": "و",
    "ھ": "ه",
    "ۀ": "ه",
    'ة': 'ه',
    "ك": "ک",
    "ګ": "گ",
    "ڪ": "گ",
    "ټ": "ت",
    "ב": "پ",
    'ە': 'ه',
    'ې': 'ی',
    'ړ': 'ر',
    'ښ': 'س',
    'ہ': 'ه',
    'ٱ': 'ا',
    'ځ': 'خ',
    'ڵ': 'ل',
    'ٹ': 'ث',
    'څ': 'خ',
    'ڈ': 'د',
    'ډ': 'د',
    'ڕ': 'ر',
    'ۅ': 'و',
    'ڤ': 'ف',
    'ں': 'ن',
    'ڼ': 'ن',
    'ۆ': 'و',
    'ۍ': 'ی',
    #attachments
    'ﺁ': 'ا',
    'ﺆ': 'و',
    'ﺎ': 'ا',
    'ﺍ': 'ا',
    'ﺑ': 'ب',
    'ﺒ': 'ب',
    'ﺐ': 'ب',
    'ﺏ': 'ب',
    'ﭘ': 'پ',
    'ﺗ': 'ت',
    'ﺘ': 'ت',
    'ﺖ': 'ت',
    'ﺕ': 'ت',
    'ﺜ': 'ث',
    'ﺟ': 'ج',
    'ﺠ': 'ج',
    'ﺞ': 'ج',
    'ﺝ': 'ج',
    'ﭼ': 'چ',
    'ﭽ': 'چ',
    'ﺣ': 'ح',
    'ﺤ': 'ح',
    'ﺧ': 'خ',
    'ﺨ': 'خ',
    'ﺦ': 'خ',
    'ﺥ': 'خ',
    'ﺪ': 'د',
    'ﺩ': 'د',
    'ﺬ': 'ذ',
    'ﺫ': 'ذ',
    'ﺮ': 'ر',
    'ﺭ': 'ر',
    'ﺯ': 'ز',
    'ﺰ': 'ز',
    'ﮊ': 'ژ',
    'ﺳ': 'س',
    'ﺴ': 'س',
    'ﺲ': 'س',
    'ﺷ': 'ش',
    'ﺸ': 'ش',
    'ﺶ': 'ش',
    'ﺼ': 'ص',
    'ﺻ': 'ص',
    'ﺹ': 'ص',
    'ﻀ': 'ض',
    'ﻂ': 'ط',
    'ﻃ': 'ط',
    'ﻄ': 'ط',
    'ﻇ': 'ظ',
    'ﻆ': 'ظ',
    'ﻈ': 'ظ',
    'ﻋ': 'ع',
    'ﻌ': 'ع',
    'ﻊ': 'ع',
    'ﻉ': 'ع',
    'ﻏ': 'غ',
    'ﻐ': 'غ',
    'ﻓ': 'ف',
    'ﻔ': 'ف',
    'ﻒ': 'ف',
    'ﻘ': 'ق',
    'ﻗ': 'ق',
    'ﻖ': 'ق',
    'ﻕ': 'ق',
    'ﻛ': 'ک',
    'ﻜ': 'ک',
    'ﻚ': 'ك',
    'ﮐ': 'ک',
    'ﮑ': 'ك',
    'ﮏ': 'ك',
    'ﮔ': 'گ',
    'ﮕ': 'گ',
    'ﮓ': 'گ',
    'ﮚ': 'گ',
    'ﻟ': 'ل',
    'ﻞ': 'ل',
    'ﻠ': 'ل',
    'ﻝ': 'ل',
    'ﻼ': 'لا',
    'ﻣ': 'م',
    'ﻤ': 'م',
    'ﻡ': 'م',
    'ﻢ': 'م',
    'ﻧ': 'ذ',
    'ﻨ': 'ذ',
    'ﻥ': 'ن',
    'ﻦ': 'ن',
    'ﻪ': 'ه',
    'ﻫ': 'ه',
    'ﻬ': 'ه',
    'ﻩ': 'ه',
    'ﮭ': 'ه',
    'ﮪ': 'ه',
    'ﮧ': 'ی',
    'ﻮ': 'و',
    'ﻭ': 'و',
    'ﻰ': 'ی',
    'ﻳ': 'ی',
    'ﻴ': 'ی',
    'ﻲ': 'ی',
    'ﻱ': 'ی',
    'ﯽ': 'ی',
    'ﯾ': 'ی',
    'ﯿ': 'ی',
    'ﯼ': 'ی',
    'ے': 'ه',
    'ﮯ': 'ی',
    #numbers
    '٤': '۴',
    '٥': '۵',
    '٦': '۶',
    '0': '۰',
    '1': '۱',
    '2': '۲',
    '3': '۳',
    '4': '۴',
    '5': '۵',
    '6': '۶',
    '7': '۷',
    '8': '۸',
    '9': '۹'
}

#source: https://www.loc.gov/catdir/cpso/romanization/bulgarian.pdf
bulgarian_transliteration = {
    'ch': 'ч',
    'ja': 'я',
    'ju': 'ю',
    'kh': 'х',
    'sht': 'щ',
    'sht': 'щ',
    'sh': 'ш',
    'ya': 'я',
    'yu': 'ю',
    'zh': 'ж',
    'a': 'а',
    'b': 'б',
    'c': 'ц',
    'd': 'д',
    'e': 'е',
    'f': 'ф',
    'g': 'г',
    'h': 'х',
    'i': 'и',
    'j': 'й',
    'k': 'к',
    'l': 'л',
    'm': 'м',
    'n': 'н',
    'o': 'о',
    'p': 'п',
    'r': 'р',
    's': 'с',
    't': 'т',
    'u': 'у',
    'v': 'в',
    'x': 'х',
    'y': 'й',
    'z': 'з',
    'ŭ': 'Ъ',
    '′': 'ь',
    '″': 'ъ',
    'i͡e': 'ѣ',
    'i͡a': 'я',
    'i͡u': 'ю',
    'ĭ': 'й',
    'u̐': 'ѫ'
}

farsi_transliteration = {
    'ء': "'",
    'آ': "|",
    'أ': "^",
    'ؤ': "W",
    'ئ': "}",
    'ا': "A",
    'ب': "b",
    'پ': "p",
    'ت': "t",
    'ث': "v",
    'ج': "J",
    'چ': "C",
    'ح': "H",
    'خ': "x",
    'د': "d",
    'ذ': "+",
    'ر': "r",
    'ز': "z",
    'ژ': "c",
    'س': "s",
    'ش': "$",
    'ص': "S",
    'ض': "D",
    'ط': "T",
    'ظ': "Z",
    'ع': "E",
    'غ': "g",
    'ف': "f",
    'ق': "q",
    'ک': "Q",
    'گ': "G",
    'ل': "l",
    'م': "m",
    'ن': "n",
    'ه': "h",
    'و': "w",
    'ی': "y",
    'ً': "F",
    "'": "%",
    '_': "_",
#    '‌': "=",
}

def process(language, text, letters_to_keep='', letters_to_remove='', lowercase=False, remove_repetitions_count=-1, remove_punct=False, remove_digits=False, remove_vowels=False, remove_diacritics=True, remove_spaces=False, remove_apostrophe=False, copy_through=True, keep_romanized_text=True):
    '''
    Normalization and cleaning-up text
    '''
    alphabet = None
    vowels = None
    language = language.upper()
    if language == 'ENGLISH' or language == 'ENG' or language == 'EN':
        language = "ENG"
    elif language == '1A' or language == 'SWAHILI' or language == 'SWA' or language == 'SW':
        language = "SWA"
    elif language == '1B' or language == 'TAGALOG' or language == 'TGL' or language == 'TL':
        language = "TGL"
    elif language == '1S' or language == 'SOMALI' or language == 'SOM' or language == 'SO':
        language = "SOM"
    elif language == '2B' or language == 'LITHUANIAN' or language == 'LIT' or language == 'LT':
        language = "LIT"
    elif language == '2S' or language == 'BULGARIAN' or language == 'BUL' or language == 'BG':
        language = "BUL"
    elif language == '2C' or language == 'PASHTO' or language == 'PUS' or language == 'PS':
        language = "PUS"
    elif language == '3S' or language == 'FARSI' or language == 'PERSIAN' or language == 'FAS' or language == 'PER' or language == 'FA':
        language = "FAS"

    alphabet = alphabet_map[language]
    if language == 'BUL' and keep_romanized_text:
        alphabet = alphabet_map['BUL_ROM']
    if language == 'PUS' and keep_romanized_text:
        alphabet = alphabet_map['PUS_ROM']
    if language == 'FAS' and keep_romanized_text:
        alphabet = alphabet_map['FAS_ROM']
    vowels = vowels_map[language]

    '''Prepare the lists of the letters to be explictily kept and removed'''
    letters_in = list(letters_to_keep)
    letters_out = list(letters_to_remove)

    '''Remove extras, e.g., non-zero width jopiner'''
    text = re.sub(extras, '', text)

    '''Transliteration for Bulgarian'''
    if language == "BUL" and not keep_romanized_text:
        for key in bulgarian_transliteration:
            if key not in letters_in:
                text = re.sub(r''+key, bulgarian_transliteration[key], text)
                text = re.sub(r''+key.upper(), bulgarian_transliteration[key].upper(), text)

    '''Mapping for Pashto'''
    if language == "PUS":
        for key in pashto_character_mappings:
            if key not in letters_in:
                text = re.sub(r''+key, pashto_character_mappings[key], text)

    '''Mapping for Farsi'''
    if language == "FAS":
        for key in farsi_character_mappings:
            if key not in letters_in:
                text = re.sub(r''+key, farsi_character_mappings[key], text)

    '''Lower-case text, if required'''
    if lowercase == True:
        text = text.lower()

    '''Remove repititions of a specific length, if required'''
    if remove_repetitions_count > 0:
        replacement = ''
        for count in range(remove_repetitions_count):
            replacement += '\\1'
        text = re.sub(r'(.)\1{'+str(remove_repetitions_count)+',}', replacement, text)

    '''Remove punctuation marks, if required'''
    if remove_punct == True:
        text = re.sub(punctuation_symbol, '', text)
        text = re.sub("(^|\s)[\']", '\1', text)

    '''Remove digits, if required'''
    if remove_digits == True:
        tokens = text.split()
        no_numbers = []
        for token in tokens:
            if not re.match(number, token):
                no_numbers.append(token)
        text = ' '.join(no_numbers)
        text = re.sub(digit, '', text)

    '''Remove apostrophe, if required'''
    if remove_apostrophe == True:
        text = re.sub('\'', '', text)

    '''Remove spaces, if required.'''
    if remove_spaces == True:
        text = re.sub('\s', '', text)

    '''Loop over the unique characters in the text'''
    for char in list(set(text)):
        #Special handling for zero-width non-joiner (do not replace)
        #if (language == 'PUS' or language == "FAS") and ord(char) == 8204:
        #    continue

        if (not char.isspace() and not re.match("[^\w\s]", char) and not re.match(punctuation_symbol, char) and not re.match(digit, char)) or char in alphabet:
            char_lower = char.lower()
            '''If the character is needed to be removed, remove it'''
            if char in letters_out:
                text = re.sub(re.escape(char), '', text)
                continue

            '''Remove diacritics, if required.'''
            if char not in letters_in and remove_diacritics:
                lower = char == char.lower()
                char_norm = char
                if char_lower in latin_character_mappings:
                    char_norm = latin_character_mappings[char_lower]
                elif language == 'PUS' and char_lower in pashto_diac:
                    char_norm = ''
                elif language == 'FAS' and char_lower in farsi_diac:
                    char_norm = ''
                elif char_lower not in alphabet:
                    char_norm_nfd = unicodedata.normalize('NFD', char_lower)
                    char_norm_ascii = char_norm_nfd.encode('ascii', 'ignore')
                    char_norm_ascii = char_norm_ascii.decode("utf-8")
                    char_norm = char_norm_ascii
                    if len(char_norm) == 0:
                        char_norm = char_norm_nfd
                    if char_norm == ' ':
                        char_norm = char_lower
                if not lower:
                    char_norm = char_norm.upper()
                if char != char_norm:
                    text = re.sub(re.escape(char), char_norm, text)
                    char = char_norm

            '''Remove vowels, if required.'''
            if char not in letters_in and remove_vowels:
                char_norm = char
                if char_lower in vowels:
                    char_norm = ''
                if char != char_norm:
                    text = re.sub(re.escape(char), char_norm, text)
                    char = char_norm

            ''' Remove any character that is not in the alphabet, if otherwise specified'''
            if not copy_through and char not in letters_in and (char in letters_out or char_lower not in alphabet):
                text = re.sub(re.escape(char), '', text)

    '''Remove extra spaces'''
    text = re.sub('\s+', ' ', text).strip()
    
    return text
