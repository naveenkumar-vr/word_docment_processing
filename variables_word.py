from nltk.tokenize import WordPunctTokenizer

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'
BOLD = WORD_NAMESPACE + 'b'
RUN = WORD_NAMESPACE + 'r'
ITALIC = WORD_NAMESPACE + 'i'
word_punct_tokenizer = WordPunctTokenizer()
