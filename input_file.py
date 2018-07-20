from token_offset import *

files = raw_input("Enter the file name: ")
path_files = raw_input("Enter the path to file: ")
text_dict = document(path_file=path_files, file=files)
print text_dict.para_dict()
