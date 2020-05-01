# coding=utf-8

import normalization

text = "tai mažas testas, taip vaikinaiūy ĖŠ aąbcčdeęėfghiįyjklmnoprsštuųūvzž"
normalized_text = normalization.process('LT', text, letters_to_keep='', letters_to_remove='', lowercase=False, remove_repetitions_count=-1, remove_punct=False, remove_digits=False, remove_vowels=False, remove_diacritics=True, remove_spaces=False, remove_apostrophe=False, copy_through= True, keep_romanized_text=True)
print(normalized_text)

text = "Côte d'Ivoire ۶ 汉字 I need to keep these line ĖŠ من من په لښ قق٤قفققكرگاه كې د پوليففسود لومړى امن سيتي  abcحوزې له   آآ آمرسره مركه ٪ من. ؟. من ،  مَن مٍن ل  ١٢٣٤٥٦ ۴ ۴ مممممممم '''This is some test "
normalized_text = normalization.process("PS", text, copy_through=False, remove_diacritics=True)
print(normalized_text)
