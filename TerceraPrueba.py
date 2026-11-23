import ee

# 1. Inicializar con tu proyecto
ee.Initialize(project='proyecto-amazonia-mariana')

# 2. Coordenadas de San José del Guaviare
punto_estudio = ee.Geometry.Point([-72.64, 2.56])

# 3. Buscar la mejor imagen de 2024
imagen = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterBounds(punto_estudio)
    .filterDate('2024-01-01', '2024-12-31')
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
    .sort('CLOUDY_PIXEL_PERCENTAGE')
    .first())

# 4. Configurar cómo queremos ver la imagen (Brillo y Bandas)
parametros_visor = {
    'bands': ['B4', 'B3', 'B2'], # Rojo, Verde, Azul
    'min': 0,
    'max': 3000,
    'gamma': 1.4,
    'region': punto_estudio.buffer(5000).bounds(), # Ver 5km alrededor
    'dimensions': 512,
    'format': 'jpg'
}

# 5. Generar el Link
url = imagen.getThumbURL(parametros_visor)

print("-------------------------------------------")
print("¡LINK GENERADO CON ÉXITO!")
print("Copia y pega este enlace en tu navegador:")
print(url)
print("-------------------------------------------")