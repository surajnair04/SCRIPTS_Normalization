'''
Updated on April 9th, 2020

@author: reskander
'''
# coding=utf-8

import sys
import re
import unicodedata

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

pashto_alphabet = "واهدرنلیيېمکتپسبخړشغچزګفځعښټډحڅجقږصۍژطكئضىظڼثذآ۶گہؤےءةأھۀإﺉًٌٍَُِّْ"
pashto_romanized_alphabet = "abcdefghijklmnopqrstuvwxyzواهدرنلیيېمکتپسبخړشغچزګفځعښټډحڅجقږصۍژطكئضىظڼثذآ۶گہؤےءةأھۀإﺉًٌٍَُِّْ"
pashto_vowels = "واېيىیےۍ"
pashto_diacs = "ًٌٍَُِّْ"

#farsi_alphabet = "ءآأؤئابپتثجچححخدذرزژسشصضطظعغفقکگلمنهویًٔ_"
farsi_alphabet = "ﻭﺎﻫﺩﺮﻨﻟیﻱېﻡکﺕپﺲﺒﺧﺶﻏچﺯﻑﻉﺡﺞﻗﺹۍژﻂﻜﺌﺿﻰﻇﺙﺫﺁ۶گہﺅےﺀﺓﺃھۀﺇﺉًَﺀﺁﺃﺆﺋﺎﺑپﺖﺜﺟچﺢﺤﺧﺩﺫﺭﺯژﺲﺸﺼﻀﻄﻈﻌﻐﻔﻗکگﻞﻤﻨﻫﻭیًٔ_"
#farsi_romanized_alphabet = "abcdefghijklmnopqrstuvwxyzﺀﺁﺃﺆﺋﺎﺑپﺖﺜﺟچﺢﺤﺧﺩﺫﺭﺯژﺲﺸﺼﻀﻄﻈﻌﻐﻔﻗکگﻞﻤﻨﻫﻭیًٔ_'|^W}AJCH+$SDTZEQGF%_="
farsi_romanized_alphabet = "abcdefghijklmnopqrstuvwxyzﻭﺎﻫﺩﺮﻨﻟیﻱېﻡکﺕپﺲﺒﺧﺶﻏچﺯﻑﻉﺡﺞﻗﺹۍژﻂﻜﺌﺿﻰﻇﺙﺫﺁ۶گہﺅےﺀﺓﺃھۀﺇﺉًَﺀﺁﺃﺆﺋﺎﺑپﺖﺜﺟچﺢﺤﺧﺩﺫﺭﺯژﺲﺸﺼﻀﻄﻈﻌﻐﻔﻗکگﻞﻤﻨﻫﻭیًٔ_'|^W}AJCH+$SDTZEQGF%_="
farsi_vowels = "‬ًًٌَُِّْﻭﺍېﻱﻯیےۍ"
farsi_diacs = ""

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
    'ﺉ': 'ئ',
    'ء': '۶',
    'ہ': 'ه',
    'ھ': 'ه',
    '۵': '٥',
    '۴': '٤',
    'ٸ': 'ئ',
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
}

farsi_character_mappings = {
    'ﺁ': "ا",
    'ﺃ': "ا",
    'ا': "آ",
    'ٓا': "آ",
    'ي': "ی",
    'ﺅ': "و",
    'ﺉ': "ی",
    'ﭘ': "پ",
    'ﻕ': 'ک',
    'ﻑ': 'پ',
    'ﻙ': 'ک',
    'گ': 'ګ',
    'ﺉ': 'ﺉ',
    'ﺀ': '۶',
    'ہ': 'ﻩ',
    'ھ': 'ﻩ',
    '۵': '٥',
    '۴': '٤',
    'ٸ': 'ﺉ',
    'ﺅ': 'ﻭ',
    'ﻻ': 'ﻻ',
    'ۓ': 'ﻱ',
    'ے': 'ﻱ',
    'ﮮ': 'ﻱ',
    'ۍ': 'ﻱ',
    'ی': 'ﻱ',
    'ﻯ': 'ﻱ',
    'ې': 'ﻱ',
    'ﺇ': 'ﺍ',
    'ﺁ': 'ﺍ',
    'ﺃ': 'ﺍ',
    'ﺓ': 'ﻩ',
    'ۀ': 'ﻩ',
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
    '‌': "=",
}

def process(language, text, letters_to_keep='', letters_to_remove='', lowercase=True, remove_repetitions_count=-1, remove_punct=True, remove_digits=True, remove_vowels=False, remove_diacritics=True, remove_spaces=False, remove_apostrophe=True, copy_through=True, keep_romanized_text=True):
    '''
    Normalization and cleaning-up text
    '''
    alphabet = None
    vowels = None
    language = language.upper()
    if (language == 'ENGLISH') or (language == 'ENG') or (language == 'EN'):
        language = "ENG"
    elif (language == '1A') or (language == 'SWAHILI') or (language == 'SWA') or (language == 'SW'):
        language = "SWA"
    elif (language == '1B') or (language == 'TAGALOG') or (language == 'TGL') or (language == 'TL'):
        language = "TGL"
    elif (language == '1S') or (language == 'SOMALI') or (language == 'SOM') or (language == 'SO'):
        language = "SOM"
    elif (language == '2B') or (language == 'LITHUANIAN') or (language == 'LIT') or (language == 'LT'):
        language = "LIT"
    elif (language == '2S') or (language == 'BULGARIAN') or (language == 'BUL') or (language == 'BG'):
        language = "BUL"
    elif (language == '2C') or (language == 'PASHTO') or (language == 'PUS') or (language == 'PS'):
        language = "PUS"
    elif (language == '3S') or (language == 'FARSI') or (language == 'FAS') or (language == 'FA'):
        language = "FAS"
        
    alphabet = alphabet_map[language]
    if language == 'BUL' and keep_romanized_text:
        alphabet = alphabet_map['BUL_ROM']
    if language == 'PUS' and keep_romanized_text:
        alphabet = alphabet_map['PUS_ROM']
    if language == 'FAS' and keep_romanized_text:
        alphabet = alphabet_map['FAS_ROM']
    vowels = vowels_map[language]

    if language == "BUL" and not keep_romanized_text:
        for key in bulgarian_transliteration:
            text = re.sub(r''+key, bulgarian_transliteration[key], text)
            text = re.sub(r''+key.upper(), bulgarian_transliteration[key].upper(), text)

    if language == "PUS":
        for key in pashto_character_mappings:
            text = re.sub(r''+key, pashto_character_mappings[key], text)

    if language == "FAS":
        for key in farsi_character_mappings:
            text = re.sub(r''+key, farsi_character_mappings[key], text)
                
    '''Prepare the lists of the letters to be explictily kept and removed'''
    letters_in = list(letters_to_keep)
    letters_out = list(letters_to_remove)
    
    '''Lower-case text, if required'''
    if lowercase == True:
        text = text.lower()
    
    '''Remove repititions of a specific length, if required'''
    if remove_repetitions_count > 0:
        replacement = r''
        for count in range(remove_repetitions_count):
            replacement += '\\1'
        text = re.sub(r'(.)\1{'+str(remove_repetitions_count)+',}', replacement, text)

    '''Remove punctuation marks, if required'''
    if remove_punct == True:
        text = re.sub(r"[^\w\s\'\َ\ً\ُ\ِ\ْ\ّ\ٌ\ٍ]",'', text)
        text = re.sub(r"(^|\s)[\']", r'\1', text)

    '''Remove digits, if required'''
    if remove_digits == True:
        text = re.sub(r'\d', '', text)

    '''Remove apostrophe, if required'''
    if remove_apostrophe == True:
        text = re.sub(r'\'', '', text)

    '''Remove spaces, if required.''' 
    if remove_spaces == True:
        text = re.sub(r'\s', '', text)

    '''Loop over the unique characters in the text'''
    for char in list(set(text)):
        #Special handling for zero-width non-joiner (do not replace)
        if (language == 'PUS' or language == "FAS") and ord(char) == 8204:
            continue
        if not char.isspace() and not char.isdigit() and not re.match(r"[^\w\s\'\َ\ً\ُ\ِ\ْ\ّ\ٌ\ٍ\d]", char):
            '''If the character is needed to be removed, remove it'''
            if char in letters_out:
                text = re.sub(re.escape(char), '', text)
                continue

            '''Remove vowels, if required.'''
            if char not in letters_in and remove_vowels:
                char_norm = char
                if char.lower() in vowels:
                    char_norm = ''
                if char != char_norm:
                    text = re.sub(re.escape(char), char_norm, text)
                    char = char_norm

            '''Remove diacritics, if required.'''
            if char not in letters_in and remove_diacritics:
                lower = char == char.lower()
                char_norm = char
                if char.lower() in latin_character_mappings:
                    char_norm = latin_character_mappings[char.lower()]
                elif char.lower() in pashto_diacs and language == "PUS":
                    char_norm = ''
                elif char.lower() in farsi_diacs and language == "FAS":
                    char_norm = ''
                elif char.lower() not in alphabet:
                    char_norm_nfd = unicodedata.normalize('NFD', char.lower())
                    char_norm_ascii = char_norm_nfd.encode('ascii', 'ignore')
                    char_norm_ascii = char_norm_ascii.decode("utf-8")
                    char_norm = char_norm_ascii
                    if len(char_norm) == 0:
                        char_norm = char_norm_nfd
                    if char_norm == ' ':
                        char_norm = char.lower()
                if not lower:
                    char_norm = char_norm.upper()
                if char != char_norm:
                    text = re.sub(re.escape(char), char_norm, text)
                    char = char_norm

            ''' Remove any character that is not in the alphabet, if otherwise specified'''
            if not copy_through and char not in letters_in and (char in letters_out or char.lower() not in alphabet):
                text = re.sub(re.escape(char), '', text)

    '''Remove extra spaces'''
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
