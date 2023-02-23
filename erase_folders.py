import os
import glob
from zipfile import ZipFile
import fnmatch
import shutil

#getting the list of folders that contains shapes
src_dir = os.path.abspath(r'/home/vitor/Documentos/Importacao_legado/')
list_files = []

for dirpath, dirnames, files in os.walk(src_dir):
    for filename in files:
        if fnmatch.fnmatch(filename, '*.zip'):
            #if fnmatch.fnmatch(str.lower(filename), 'aprt_*'):
                file_path = os.path.join(dirpath, filename)
                list_files.append(file_path)
                #print(file_path)

to_erase = []

for file_path in list_files:
    if file_path not in to_erase:
        to_erase.append(os.path.dirname(file_path))
print(to_erase)

for folder in to_erase:
    try:
        shutil.rmtree(folder)
    except Exception as e:
        print("Not found", e)