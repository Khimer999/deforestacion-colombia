import ee

# 1. Inicializar
ee.Initialize(project='proyecto-amazonia-mariana')

# 2. Área de estudio (Un cuadrado de 5km x 5km)
punto = ee.Geometry.Point([-72.64, 2.56])
area_estudio = punto.buffer(5000).bounds()

def get_ndvi(img):
    return img.normalizedDifference(['B8', 'B4'])

# 3. Traer las mejores imágenes de cada año
img_2019 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterBounds(area_estudio).filterDate('2019-01-01', '2019-12-31').sort('CLOUDY_PIXEL_PERCENTAGE').first()
img_2024 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterBounds(area_estudio).filterDate('2024-01-01', '2024-12-31').sort('CLOUDY_PIXEL_PERCENTAGE').first()

# 4. Calcular NDVI para ambos años
ndvi_2019 = get_ndvi(img_2019)
ndvi_2024 = get_ndvi(img_2024)

# 5. Máscara de pérdida: Era bosque (>0.6) y ya no lo es (<0.6)
bosque_2019 = ndvi_2019.gt(0.6)
bosque_2024 = ndvi_2024.gt(0.6)
perdida = bosque_2019.And(bosque_2024.Not())

# 6. Contar los píxeles de pérdida
stats = perdida.reduceRegion(
    reducer=ee.Reducer.sum(),
    geometry=area_estudio,
    scale=10, # Resolución de Sentinel-2 (10m por píxel)
    maxPixels=1e9
)

pixeles_perdidos = stats.get('nd').getInfo()
hectareas = (pixeles_perdidos * 100) / 10000 # Cada píxel son 100m2

print("-------------------------------------------")
print(f"Píxeles de bosque perdidos: {int(pixeles_perdidos)}")
print(f"Equivalente en hectáreas: {hectareas:.2f} ha")
print("-------------------------------------------")