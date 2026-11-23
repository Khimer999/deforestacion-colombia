import ee

# 1. Inicializar con tu proyecto
ee.Initialize(project='proyecto-amazonia-mariana')

# 2. Definir las coordenadas de San José del Guaviare
punto_estudio = ee.Geometry.Point([-72.64, 2.56])

# 3. AQUÍ ESTÁ EL NOMBRE CORREGIDO:
coleccion = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterBounds(punto_estudio)
    .filterDate('2024-01-01', '2024-12-31')
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
    .sort('CLOUDY_PIXEL_PERCENTAGE'))

# 4. Obtener la mejor imagen
imagen = coleccion.first()

if imagen:
    print("¡Conexión exitosa y datos filtrados!")
    print(f"ID de la imagen: {imagen.id().getInfo()}")
else:
    print("No se encontraron imágenes sin nubes en esa zona.")