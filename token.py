from lxml import etree
from collections import OrderedDict
from nltk.tokenize import WordPunctTokenizer

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'
word_punct_tokenizer = WordPunctTokenizer()

def token_offsets(text):
    l1= []
    l = []
    for i in range(len(text)):
        if text[i] == ' ':
            l1.append(l)
            l = []
        else:
            l.append(i)
    l1.append(l)
    l1 = [x for x in l1 if x != []]
    temp = []
    for j in range(len(l1)):
        if len(l1[j]) > 2:
            temp.append(l1[j][0])
            temp.append(l1[j][-1])
            l1[j] = temp
            temp = []
    return l1

def check_and_embed_ids_in_paras(xml):
#    """ Checks of unique ids are present in the paragraphs of the given main document, if not - embeds them"""

    text_dict = OrderedDict()
    tree = etree.ElementTree(file=xml)
    id_number = 0

    for para in tree.iter(PARA):
        if para.attrib.get('id') is None:
            para.attrib['id'] = str(id_number)
            id_number += 1
        texts = [node.text for node in para.iter(TEXT) if node.text]
        if texts:
            para_text = ''.join(texts).strip()
            text_dict[para.attrib['id']] = {}
            text_dict[para.attrib['id']]['text'] = para_text
            text_dict[para.attrib['id']]['token_offsets'] = token_offsets(para_text)
            text_dict[para.attrib['id']]['tokens'] = word_punct_tokenizer.tokenize(para_text)

    tree.write(xml, encoding='UTF-8', standalone=True, pretty_print=True)

    return text_dict
a = raw_input()
print check_and_embed_ids_in_paras(a)
