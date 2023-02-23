import os
import glob
from zipfile import ZipFile
import fnmatch

#getting the list of folders that contains shapes
src_shapefiles = os.path.abspath(r'/home/guilherme/Documents/Fazendas Legado/')
shapefiles = []

for dirpath, dirnames, files in os.walk(src_shapefiles):
    for filename in files:
        if fnmatch.fnmatch(filename, '*.shp'):
            if fnmatch.fnmatch(str.lower(filename), 'aprt_*'):
                shapefile = os.path.join(dirpath, filename)
                shapefiles.append(shapefile)

# remove duplicates from the list
unique_shapefiles = list(set(shapefiles))

# get the unique folders that contain the shapefiles
unique_folders = []
for shapefile in unique_shapefiles:
    folder = os.path.dirname(shapefile)
    if folder not in unique_folders:
        unique_folders.append(folder)


# iterate through each input directory
for unique_folder in unique_folders:

    # define the destination directory for the zip files
    dest = os.path.join(unique_folder, "zips")
    
    # change the current directory to the input directory
    os.chdir(unique_folder)

    # list all files with extension .shp
    shps = glob.glob(unique_folder + "/aprt_*.shp")

    # create empty list for zipfile names
    ziplist = []

    # create destination directory if it does not exist
    if not os.path.exists(dest):
        os.makedirs(dest)

    # populate ziplist list of unique shapefile root names by finding all files with .shp extension and removing extension
    for name in shps:
        # retrieves just the files name for each name in shps
        file = os.path.basename(name)
        # removes .shp extension
        names = file[:-4]
        # adds each shapefile name to ziplist list
        ziplist.append(names)

    # creates zipefiles in dest folder with basenames
    for f in ziplist:
        # creates the name for each zipefile based on shapefile root names
        file_name = os.path.join(dest, f + ".zip")
        # created the zipfiles with names defined above
        with ZipFile(file_name, "w") as zips:
            # files lists all files with the current basename (f) from ziplist
            files = glob.glob(os.path.join(unique_folder, str(f) + ".*"))
            # iterate through each basename and add all shapefile components to the zipefile
            for s in files:
                zips.write(s, os.path.basename(s))