import os
from osgeo import ogr, osr

src_shapefiles = os.path.abspath(r'/home/guilherme/Documents/Fazendas Legado/')
shapefiles = []



for dirpath, dirnames, files in os.walk(src_shapefiles):
    for filename in files:
        if filename.endswith('APRT.shp'):
            shapefile = os.path.join(dirpath, filename)
            shapefiles.append(shapefile) # append file path to list

print(shapefiles)
print(len(shapefiles))

# Define the WGS84 spatial reference
projection = osr.SpatialReference()
projection.ImportFromEPSG(4326)

# Loop through the list of src_shapefiles
for shapefile in shapefiles:
    try:
        src_ds = ogr.Open(shapefile)
        if src_ds is None:
            print(f"Could not open {shapefile}")
            continue
        src_layer = src_ds.GetLayer()
        
    except AttributeError as e:
        print(f"Error processing {shapefile}: {e}")

    # Path to the new shapefile
    dst_shapefile = os.path.dirname(shapefile) +"//"+ "aprt_limite_" + os.path.basename(shapefile)

    # Create the new shapefile
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dst_ds = driver.CreateDataSource(dst_shapefile)

    # Define the new shapefile's spatial reference
    dst_sr = projection

    # Create the new shapefile's layer
    dst_layer = dst_ds.CreateLayer("limite", dst_sr, ogr.wkbPolygon)

    # Add the fields to the new shapefile's layer
    field_fazenda = ogr.FieldDefn("fazenda", ogr.OFTString)
    field_fazenda.SetWidth(254)
    dst_layer.CreateField(field_fazenda)

    field_proprietar = ogr.FieldDefn("proprietar", ogr.OFTString)
    field_proprietar.SetWidth(254)
    dst_layer.CreateField(field_proprietar)

    field_municipio = ogr.FieldDefn("municipio", ogr.OFTString)
    field_municipio.SetWidth(35)
    dst_layer.CreateField(field_municipio)

    field_estado = ogr.FieldDefn("estado", ogr.OFTString)
    field_estado.SetWidth(30)
    dst_layer.CreateField(field_estado)

    field_x = ogr.FieldDefn("x", ogr.OFTReal)
    field_x.SetPrecision(15)
    dst_layer.CreateField(field_x)

    field_y = ogr.FieldDefn("y", ogr.OFTReal)
    field_y.SetPrecision(15)
    dst_layer.CreateField(field_y)

    field_codigo = ogr.FieldDefn("codigo", ogr.OFTString)
    field_codigo.SetWidth(30)
    dst_layer.CreateField(field_codigo)

    # Copy the features from the source shapefile to the new shapefile
    try:
        for src_feature in src_layer:
            if src_feature is not None:
                dst_feature = ogr.Feature(dst_layer.GetLayerDefn())

            fields_to_copy = ["Fazenda", "Proprietár", "Município", "Estado"]

            for field in fields_to_copy:
                try:
                    value = src_feature.GetField(str(field))
                    if isinstance(value, str):
                        dst_feature.SetField("descricao", value)
                    else:
                        print("Not a String")
                        continue
                except KeyError as e:
                    print(f"An error occurred while setting the {field} field value: {str(e)}")
                except Exception as e:
                    print(f"An unexpected error occurred while setting the {field} field value: {str(e)}")
                    continue


            
            try:
                dst_layer.CreateFeature(dst_feature)
            except AttributeError as e:
                print(f"An error occurred while creating the feature: {str(e)}")
    except AttributeError as e:
        print(f"An error occurred: {str(e)}")


        # reset dst_feature to free resources
        dst_feature = None

        try:
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

        except AttributeError as e:
            print("Error:", str(e))
            continue

    # Clean up
    src_ds = None
    dst_ds = None