 # Proyecto de Simulación de Centro Logístico
 
 ## Descripción
 
 Este proyecto simula un centro logístico donde vehículos llegan a estaciones de carga y utilizan montacargas para posicionarse, operar y retirarse.
 
 El objetivo principal es estimar el tiempo promedio de espera de los vehículos y analizar la utilización de los recursos.
 
 ## Estructura del proyecto
 
 ```
 Simulacion/
 ├── parametros.py        # Configuración de parámetros
 ├── entidades.py         # Definición de vehículos y estadísticas
 ├── terminal.py          # Lógica de simulación
 ├── analisis.py          # Análisis estadístico de resultados
 ├── ejecutar.py          # Ejecución principal y guardado de resultados
 ├── inicio.py            # Punto de entrada principal
 ├── requirements.txt     # Dependencias
 └── README.md            # Este archivo
 ```
 
 ## Requisitos
 
 - Python 3.7 o superior
 - pip
 
 Instalar dependencias:
 
 ```bash
 pip install -r requirements.txt
 ```
 
 Para generar el PDF se requiere una instalación de LaTeX compatible (MiKTeX en Windows, TeX Live en Linux/macOS).
 
 ## Uso
 
 Ejecutar la simulación:
 
 ```bash
 python inicio.py
 ```
 
 Esto ejecutará varias réplicas de simulación, calculará estadísticas y guardará un archivo `resultados_simulacion.txt`.

 
 ```bash
 python generar_informe.py
 ```
 
 ## Parámetros configurables
 
 Modificar `parametros.py` para ajustar:
 
 - `CANTIDAD_ESTACIONES_CARGA` - Número de estaciones de carga
 - `CANTIDAD_MONTACARGAS` - Número de montacargas disponibles
 - `TIEMPO_SIMULACION_HORAS` - Duración de cada réplica de simulación
 - `CANTIDAD_REPLICAS` - Número de réplicas para análisis estadístico
 - `MEDIA_LLEGADA_HORAS` - Tiempo promedio entre llegadas de vehículos
 
 ## Componentes
 
 - `entidades.py`: define la clase `Vehiculo` y `EstadisticasOperacion`
 - `terminal.py`: simula la llegada y el ciclo completo de cada vehículo
 - `analisis.py`: calcula intervalos de confianza y resume métricas
 - `ejecutar.py`: ejecuta réplicas, imprime resultados y guarda texto
 
 ## Resultados esperados
 
 La simulación entrega:
 
 1. Tiempo promedio de espera desde llegada hasta inicio de operación
 2. Tiempo promedio total en el sistema
 3. Cantidad promedio de vehículos procesados
 4. Utilización de estaciones de carga y montacargas
 5. Intervalos de confianza del 95%

