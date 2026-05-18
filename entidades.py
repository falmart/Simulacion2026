import random
import math
from parametros import CATEGORIAS, PROBABILIDADES_CATEGORIA, MEDIA_OPERACION, VARIANZA_OPERACION


class Vehiculo:
    _contador_ids = 0
    
    def __init__(self, momento_llegada):
        Vehiculo._contador_ids += 1
        self.id = Vehiculo._contador_ids
        self.momento_llegada = momento_llegada
        
        # Determinar categoría según probabilidades
        self.categoria = random.choices(CATEGORIAS, PROBABILIDADES_CATEGORIA)[0]
        
        # Generar tiempo de operación según distribución normal
        media = MEDIA_OPERACION[self.categoria]
        varianza = VARIANZA_OPERACION[self.categoria]
        desviacion = math.sqrt(varianza)
        
        # Aseguramos que el tiempo no sea negativo
        self.tiempo_operacion = max(0.1, random.gauss(media, desviacion))
        
        # Variables para seguimiento temporal
        self.momento_inicio_operacion = None
        self.momento_fin_operacion = None
        self.momento_inicio_posicionamiento = None
        self.momento_fin_posicionamiento = None
        self.momento_inicio_despliegue = None
        self.momento_fin_despliegue = None
        
        # Estado actual
        self.estacion_asignada = None
        self.estado = "esperando"  # esperando, en_montacargas_entrada, operando, en_montacargas_salida, finalizado
    
    @property
    def tiempo_espera(self):
        if self.momento_inicio_operacion is not None:
            return self.momento_inicio_operacion - self.momento_llegada
        return None
    
    @property
    def tiempo_total_sistema(self):
        """Tiempo total desde llegada hasta fin de despliegue"""
        if self.momento_fin_despliegue is not None:
            return self.momento_fin_despliegue - self.momento_llegada
        return None
    
    def __repr__(self):
        return f"Vehiculo({self.id}, {self.categoria}, llegó en t={self.momento_llegada:.2f})"


class EstadisticasOperacion:
    def __init__(self):
        self.vehiculos_procesados = []
        self.tiempos_espera = []
        self.tiempos_sistema = []
        self.utilizacion_estaciones = []
        self.utilizacion_grua = None
        self.numero_vehiculos_cola = []
        
    def registrar_vehiculo(self, vehiculo):
        self.vehiculos_procesados.append(vehiculo)
        if vehiculo.tiempo_espera is not None:
            self.tiempos_espera.append(vehiculo.tiempo_espera)
        if vehiculo.tiempo_total_sistema is not None:
            self.tiempos_sistema.append(vehiculo.tiempo_total_sistema)
    
    @property
    def tiempo_espera_promedio(self):
        if not self.tiempos_espera:
            return 0
        return sum(self.tiempos_espera) / len(self.tiempos_espera)
    
    @property
    def tiempo_sistema_promedio(self):
        if not self.tiempos_sistema:
            return 0
        return sum(self.tiempos_sistema) / len(self.tiempos_sistema)
    
    @property
    def total_vehiculos_procesados(self):
        return len(self.vehiculos_procesados)
