from zipfile import ZipFile

path = " "
path = raw_input("Enter the path: ")
zip = ZipFile(path,'r')
zip.extractall()
