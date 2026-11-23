import ee

# 1. Inicializar
ee.Initialize(project='proyecto-amazonia-mariana')

# 2. Localización y búsqueda de imagen
punto_estudio = ee.Geometry.Point([-72.64, 2.56])
imagen = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterBounds(punto_estudio)
    .filterDate('2024-01-01', '2024-12-31')
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
    .sort('CLOUDY_PIXEL_PERCENTAGE')
    .first())

# 3. CÁLCULO MATEMÁTICO DEL NDVI
# La función normalizedDifference hace la fórmula (B8 - B4) / (B8 + B4)
ndvi = imagen.normalizedDifference(['B8', 'B4']).rename('NDVI')

# 4. Configurar el visor (Paleta de colores: Rojo = Suelo, Verde = Selva)
parametros_ndvi = {
    'min': 0,
    'max': 1,
    'palette': ['red', 'yellow', 'green'],
    'region': punto_estudio.buffer(5000).bounds(),
    'dimensions': 512,
    'format': 'jpg'
}

# 5. Generar el Link del mapa de salud
url_ndvi = ndvi.getThumbURL(parametros_ndvi)

print("-------------------------------------------")
print("¡ANÁLISIS MATEMÁTICO COMPLETADO!")
print("Este mapa muestra la salud de la selva:")
print(url_ndvi)
print("-------------------------------------------")