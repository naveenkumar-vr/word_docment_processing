from variables_word import *

class document:

    def __init__(self, path_file, file):
        self.file = file
        self.path_file = path_file
        self.text_dict = OrderedDict()
        self.token_offsets = []
        self.tokens = []
        self.xml = ''


    def unzip(self):

        zip = zipfile.ZipFile(self.path_file, 'r')
        path_extracted_file = self.path_file.replace('/' + self.file, '')
        zip.extractall(path_extracted_file)
        path_xml = self.path_file.replace(self.file, 'word')
        for root, dirs, files in os.walk(path_xml):
            if 'document.xml' in files:
                self.xml = 'document.xml'


    def token_offset(self, text):

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


    def check_and_embed_ids_in_paras(self):

        tree = etree.ElementTree(file=self.xml)
        id_number = 0
        for para in tree.iter(PARA):
            if para.attrib.get('id') is None:
                para.attrib['id'] = str(id_number)
                id_number += 1
            texts = [node.text for node in para.iter(TEXT) if node.text]
            if texts:
                para_text = ''.join(texts).strip()
                self.text_dict[para.attrib['id']] = {}
                self.text_dict[para.attrib['id']]['text'] = para_text
                copy_token_offset = self.token_offset(text=para_text)
                self.token_offsets.append(copy_token_offset)
                self.text_dict[para.attrib['id']]['token_offsets'] = copy_token_offset
                copy_token = word_punct_tokenizer.tokenize(para_text)
                self.tokens.append(copy_token)
                self.text_dict[para.attrib['id']]['tokens'] = copy_token
        return self.text_dict


    def style(self, STYLE):

        tree = etree.ElementTree(file=self.xml)
        id_number = 0
        id_number_list = []
        for para in tree.iter(PARA):
            style_text_list = []
            style_tokenoffsets = []
            texts = [node.text for node in para.iter(TEXT) if node.text]
            if texts:
                para_text = ''.join(texts).strip()
                token_offsets = self.token_offset(text=para_text)
                tokens = word_punct_tokenizer.tokenize(para_text)
            for run in para.iter(RUN):
                for style in run.iter(STYLE):
                    style_parent = style.getparent()
                    if style_parent.tag == run.tag + 'Pr':
                        style_run_text_list = [node.text for node in run.iter(TEXT) if node.text]
                        style_run_text = ''.join(style_run_text_list).strip()
                        style_text_list.append(style_run_text)
                style_text = ''.join(style_text_list).strip()
                style_tokens = word_punct_tokenizer.tokenize(style_text)
                index_style_tokenoffset = [j for i in range(len(style_tokens)) for j in range(len(tokens)) if style_tokens[i] == tokens[j]]
                style_no_true_tokenoffset = [token_offsets[i] for i in index_style_tokenoffset]
                for i in range(len(style_no_true_tokenoffset)):
                    temp = []
                    for offsets in style_no_true_tokenoffset[i]:
                        temp.append(offsets)
                    temp.append('true')
                    if temp not in style_tokenoffsets: style_tokenoffsets.append(temp)
            if texts:
                if STYLE == BOLD: self.text_dict[str(id_number)]['bold'] = style_tokenoffsets
                if STYLE == ITALIC: self.text_dict[str(id_number)]['italic'] = style_tokenoffsets
                if STYLE == UNDERLINE: self.text_dict[str(id_number)]['underline'] = style_tokenoffsets
            id_number += 1
        return self.text_dict



    def para_dict(self):
        self.unzip()
        check_and_embed_ids_in_paras = self.check_and_embed_ids_in_paras()
        bold_style = self.style(BOLD)
        italic_style = self.style(ITALIC)
        style = self.style(UNDERLINE)
        return style
