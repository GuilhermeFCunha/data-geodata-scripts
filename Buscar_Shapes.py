import pathlib
from pathlib import Path
import shutil
import os
from os import path as p

pastas = [
    'Pirapitinga'
    
    ]

feature = 'CLASS'

def copyFiles(file,filename,newExt,dest):
    dir = pathlib.Path(file).parents[0]
    otherextension = str(file).replace('shp',newExt)
    new_file_name = os.path.join(dir, dest, filename+ "." + newExt)

    if os.path.isfile(otherextension):
        shutil.copy(otherextension,new_file_name)
    pass

def createFolders():

    for pasta in  pastas:
        path = r'/home/guilherme/Documents/'+pasta
        dest = r'/home/guilherme/Documents/Class_temp/'+feature
        indice = 0

        if not os.path.exists(dest):
            os.makedirs(dest)


        for file in Path(path).glob('**/*'+feature+'*.shp'):
            filename = pathlib.Path(file).stem
            new_name = str(indice) +'_'+filename
            copyFiles(file,new_name,'shp',dest)
            copyFiles(file,new_name,'dbf',dest)
            copyFiles(file,new_name,'cpg',dest)
            copyFiles(file,new_name,'shx',dest)
            copyFiles(file,new_name,'sbn',dest)
            copyFiles(file,new_name,'sbx',dest)
            copyFiles(file,new_name,'prj',dest)
            indice = indice +1
            pass
        pass
    pass

createFolders()
    
