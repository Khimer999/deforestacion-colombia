import ee

# 1. Inicializar
ee.Initialize(project='proyecto-amazonia-mariana')

# 2. Localización: San José del Guaviare
punto_estudio = ee.Geometry.Point([-72.64, 2.56])

# 3. FUNCIÓN PARA BUSCAR LA MEJOR IMAGEN POR AÑO
def obtener_mejor_imagen(fecha_inicio, fecha_fin):
    return (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(punto_estudio)
        .filterDate(fecha_inicio, fecha_fin)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
        .sort('CLOUDY_PIXEL_PERCENTAGE')
        .first())

# 4. Obtener las dos imágenes (2019 vs 2024)
imagen_2019 = obtener_mejor_imagen('2019-01-01', '2019-12-31')
imagen_2024 = obtener_mejor_imagen('2024-01-01', '2024-12-31')

# 5. Configurar visualización (Color Verdadero)
parametros_visor = {
    'bands': ['B4', 'B3', 'B2'],
    'min': 0, 'max': 3000, 'gamma': 1.4,
    'region': punto_estudio.buffer(5000).bounds(),
    'dimensions': 512, 'format': 'jpg'
}

# 6. Generar Links
url_2019 = imagen_2019.getThumbURL(parametros_visor)
url_2024 = imagen_2024.getThumbURL(parametros_visor)

print("-------------------------------------------")
print("ANÁLISIS TEMPORAL (ANTES Y DESPUÉS)")
print(f"LINK 2019: {url_2019}")
print(f"LINK 2024: {url_2024}")
print("-------------------------------------------")