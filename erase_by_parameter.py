import os
import fnmatch

src_shapefiles = os.path.abspath(r'/home/guilherme/Documents/Fazendas Legado/')
to_erase_files = []

for dirpath, dirnames, files in os.walk(src_shapefiles):
    for filename in files:
        #if fnmatch.fnmatch(filename, '*CLASS*'):
            if fnmatch.fnmatchcase(filename.lower(), 'aprt_*'):
                shapefile = os.path.join(dirpath, filename)
                to_erase_files.append(shapefile) # append file path to list

print(to_erase_files)

for to_erase_file in to_erase_files:
    os.unlink(to_erase_file)