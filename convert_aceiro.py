import os
import fnmatch
from osgeo import ogr, osr

src_shapefiles = os.path.abspath(r'/home/guilherme/Documents/Fazendas Legado/')
shapefiles = []

for dirpath, dirnames, files in os.walk(src_shapefiles):
    for filename in files:
        if fnmatch.fnmatch(str.lower(filename), '*aceiro*'):
            if fnmatch.fnmatch(filename, '*.shp'):
                shapefile = os.path.join(dirpath, filename)
                shapefiles.append(shapefile) # append file path to list

print(shapefiles)
print(len(shapefiles))

# Define the WGS84 spatial reference
projection = osr.SpatialReference()
projection.ImportFromEPSG(4326)

# Loop through the list of src_shapefiles
for shapefile in shapefiles:
    src_ds = ogr.Open(shapefile)
    src_layer = src_ds.GetLayer()
    
    # Path to the new shapefile
    dst_shapefile = os.path.dirname(shapefile) +"//"+ "aprt_aceiro.shp"

    # Start the creation of the new shapefile
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dst_ds = driver.CreateDataSource(dst_shapefile)

    # Define the new shapefile's spatial reference
    dst_sr = projection

    # Finish the new shapefile's layer
    dst_layer = dst_ds.CreateLayer("limite", dst_sr, ogr.wkbLineString)

    # Add the fields to the new shapefile's layer
    field_descricao = ogr.FieldDefn("descricao", ogr.OFTString)
    field_descricao.SetWidth(50)
    dst_layer.CreateField(field_descricao)

    # Copy the features from the source shapefile to the new shapefile
    for src_feature in src_layer:
        dst_feature = ogr.Feature(dst_layer.GetLayerDefn())

        fields_to_copy = ["DESCRICAO", "DESCRIÇÃO"]
        for field in fields_to_copy:
            try:
                dst_feature.SetField("descricao", src_feature.GetField(field))
            except KeyError as e:
                print(f"An error occurred while setting the {field} field value: {str(e)}")

        src_geometry = src_feature.GetGeometryRef()
        if src_geometry is not None:
            dst_geometry = src_geometry.Clone()
            dst_geometry.TransformTo(dst_sr) # Transform the geometry to WGS84
            dst_geometry.SwapXY() # Invert the x and y axis
            dst_feature.SetGeometry(dst_geometry)
        else:
            print("Warning: Geometria inválida, pulando.")
            continue

        dst_layer.CreateFeature(dst_feature)

    # Clean up
    src_ds = None
    dst_ds = None