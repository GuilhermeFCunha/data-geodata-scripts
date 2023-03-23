import geopandas as gpd
from deep_translator import GoogleTranslator

# SELECIONA O ARQUIVO A SER LIDO (GDB, GEOJSON, SHAPEFILE)
exl_file = '/home/guilherme/Downloads/ecorregioes_terrestres/geojson/an.geojson'

# CRIA UM GEODATAFRAME A PARTIR DO ARQUIVO SELECIONADO
gdf = gpd.read_file(exl_file)

# CARREGA A API COMO FUNÇÃO, DETECTA O IDIOMA E SETA PARA PORTUGUÊS COMO PARÂMETROS
tradutor = GoogleTranslator(source='auto', target='pt')

# APLICA A FUNÇÃO PARA A TABELA DO GEODATAFRAME SELECIONADO
traduzido = gdf.ECO_NAME.apply(tradutor.translate)

# CRIA UMA NOVA COLUNA "ECO_NOME_TRADUZIDO" E APLICA A TRADUÇÃO A ELA
gdf = gdf.assign(ECO_NOME_TRADUZIDO = traduzido)

# SALVA O GEODATAFRAME TRATADO PARA UM NOVO ARQUIVO (GDB, GEOJSON, SHAPEFILE)
gdf.to_file('/home/guilherme/Downloads/ecorregioes_terrestres/geojson/novo_an.shp')
