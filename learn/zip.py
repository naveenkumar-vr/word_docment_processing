import os,zipfile
from zipfile import ZipFile
s_path = ""
def zipd(ziph):
    for path,dirs,files in os.walk(s_path):
        for file in files:
            l = [".xml",".txt",".docx",".py",".c",".pages",".pptx",".pdf",".doc",".zip"]
            for i in l:
                if file.endswith(i):
                    ziph.write(os.path.join(path, file))

s_path = raw_input("Enter the directory: ")
zipf = ZipFile(s_path + ".zip", 'w', zipfile.ZIP_DEFLATED)
zipd(zipf)
zipf.close()
