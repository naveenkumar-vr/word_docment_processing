import os
from lxml import etree
from zipfile import ZipFile
# from variables_word import *
from collections import OrderedDict
from nltk.tokenize import WordPunctTokenizer


WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'
BOLD = WORD_NAMESPACE + 'b'
RUN = WORD_NAMESPACE + 'r'
ITALIC = WORD_NAMESPACE + 'i'
word_punct_tokenizer = WordPunctTokenizer()


def unzip(path, file):
    zip = ZipFile(path, 'r')
    zip.extractall()
    xml = ''
    path_xml = path.replace(file, 'word')
    for root, dirs, files in os.walk(path_xml):
        if 'document.xml' in files:
            xml = 'document.xml'
    res = check_and_embed_ids_in_paras(xml)
    return res


def token_offsets(text):
    token = word_punct_tokenizer.tokenize(text)
    count = 0
    token_offset = []
    token_of_tokenoffset = [0]
    temp_text = ''
    for i in range(len(text)):
        if temp_text != token[0] and text[i] != ' ':
            temp_text += text[i]
            if token_of_tokenoffset[0] == 0:
                token_of_tokenoffset[0] += count
        if temp_text == token[0]:
            token_of_tokenoffset.append(count)
            token_offset.append(token_of_tokenoffset)
            token.remove(temp_text)
            temp_text = ''
            token_of_tokenoffset = [0]
        count += 1
    return token_offset


def check_and_embed_ids_in_paras(xml):

    text_dict = OrderedDict()
    tree = etree.ElementTree(file=xml)
    id_number = 0
    token_offset = []
    token = []
    for para in tree.iter(PARA):
        text_token = {}
        if para.attrib.get('id') is None:
            para.attrib['id'] = str(id_number)
            id_number += 1
        texts = [node.text for node in para.iter(TEXT) if node.text]
        if texts:
            para_text = ''.join(texts).strip()
            text_dict[para.attrib['id']] = {}
            text_dict[para.attrib['id']]['text'] = para_text
            token_offset1 = token_offsets(para_text)
            token_offset.append(token_offset1)
            text_dict[para.attrib['id']]['token_offsets'] = token_offset
            token1 = word_punct_tokenizer.tokenize(para_text)
            token.append(token1)
            text_dict[para.attrib['id']]['tokens'] = token
        for i in range(len(token)):
            for j in range(len(token[i])):
                text_token[token[i][j]] = token_offset[i][j]
        bold_list = []
        bold_true = []
        italic_list = []
        italic_true = []
        for run in para.iter(RUN):
            for bold in run.iter(BOLD):
                bold_parent = bold.getparent()
                if bold_parent.tag == run.tag + 'Pr':
                        bold_text = [node.text for node in run.iter(TEXT) if node.text]
                        bold_texts = ''.join(bold_text).strip()
                        bold_list.append(bold_texts)
            for italic in run.iter(ITALIC):
                italic_parent = italic.getparent()
                if italic_parent.tag == run.tag + 'Pr':
                        italic_text = [node.text for node in run.iter(TEXT) if node.text]
                        italic_texts = ''.join(italic_text).strip()
                        italic_list.append(italic_texts)
        bold_lists = ''.join(bold_list).strip()
        italic_lists = ''.join(italic_list).strip()
        bold_tokens = word_punct_tokenizer.tokenize(bold_lists)
        italic_tokens = word_punct_tokenizer.tokenize(italic_lists)
        for key, value in text_token.items():
            for text in bold_tokens:
                if text == key:
                    value.append('true')
                    bold_true.append(value)
            for text in italic_tokens:
                if text == key:
                    value.append('true')
                    italic_true.append(value)
        if texts:
            text_dict[para.attrib['id']]['bold'] = bold_true
            text_dict[para.attrib['id']]['italic'] = italic_true
    tree.write(xml, encoding='UTF-8', standalone=True, pretty_print=True)

    return text_dict


file = raw_input("Enter the file name: ")
path = raw_input("Enter the path to file: ")
print unzip(path, file)
