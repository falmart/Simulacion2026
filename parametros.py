# Configuración del centro logístico
CANTIDAD_ESTACIONES_CARGA = 3
CANTIDAD_MONTACARGAS = 1

# Llegada de vehículos (distribución exponencial, λ = 8 horas → media 8 horas)
MEDIA_LLEGADA_HORAS = 8  # 1/λ = 8 horas
TASA_LLEGADA = 1 / MEDIA_LLEGADA_HORAS  # λ = 0.125 vehículos/hora

# Categorías de vehículos
CATEGORIAS = ['ligero', 'mediano', 'pesado']
PROBABILIDADES_CATEGORIA = [0.25, 0.25, 0.5]

# Tiempo de operación de carga (distribución normal)
MEDIA_OPERACION = {
    'ligero': 9,
    'mediano': 12,
    'pesado': 18
}
VARIANZA_OPERACION = {
    'ligero': 1,
    'mediano': 2,
    'pesado': 3
}

# Asistencia de montacargas (distribución exponencial)
# - Posicionar vehículo en estación de carga: λ = 2 horas → media = 0.5 horas (30 min)
MEDIA_POSICIONAMIENTO_HORAS = 0.5
TASA_POSICIONAMIENTO = 1 / MEDIA_POSICIONAMIENTO_HORAS

# - Retirar vehículo de la estación de carga: λ = 1 hora → media = 1 hora
MEDIA_DESPLIEGUE_HORAS = 1
TASA_DESPLIEGUE = 1 / MEDIA_DESPLIEGUE_HORAS

# - Traslado vacío del montacargas: λ = 15 minutos = 0.25 horas
MEDIA_TRASLADO_VACÍO_HORAS = 0.25
TASA_TRASLADO_VACÍO = 1 / MEDIA_TRASLADO_VACÍO_HORAS

# Tiempo total de simulación (en horas)
TIEMPO_SIMULACION_HORAS = 8760  # 1 año

# Cantidad de repeticiones para análisis estadístico
CANTIDAD_REPLICAS = 30
