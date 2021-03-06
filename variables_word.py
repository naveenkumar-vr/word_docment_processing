import os
from lxml import etree
import zipfile
from zipfile import ZipFile
from collections import OrderedDict
from nltk.tokenize import WordPunctTokenizer

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'
BOLD = WORD_NAMESPACE + 'b'
RUN = WORD_NAMESPACE + 'r'
ITALIC = WORD_NAMESPACE + 'i'
UNDERLINE = WORD_NAMESPACE + 'u'
COLOR = WORD_NAMESPACE + 'color'
VALUE = WORD_NAMESPACE + 'val'
SIZE = WORD_NAMESPACE + 'sz'
PARA_Pr = WORD_NAMESPACE + 'pPr'
INDENT = WORD_NAMESPACE + 'ind'
LEFT_IND = WORD_NAMESPACE + 'left'
word_punct_tokenizer = WordPunctTokenizer()
