import normalization
import sys
from mosestokenizer import *

if __name__=="__main__":
    lang = sys.argv[1]
    tokenizer = MosesTokenizer(lang)
    punct_norm = MosesPunctuationNormalizer(lang)    
    for line in sys.stdin:
        line = line.strip()
        if not line: continue
        line = " ".join(tokenizer(punct_norm(line)))
        line = normalization.process(lang, line, copy_through=False, keep_romanized_text=False)
        print(line)
