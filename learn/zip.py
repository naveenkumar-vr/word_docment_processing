import os,zipfile
from zipfile import ZipFile
s_path = ""
def zipd(ziph):
    for path,dirs,files in os.walk(s_path):
        for file in files:
            ziph.write(os.path.join(path, file))

s_path = raw_input("Enter the directory: ")
zipf = ZipFile(s_path + ".zip", 'w')
zipd(zipf)
zipf.close()
