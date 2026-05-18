import simpy  # type: ignore[import]
import random
from parametros import (
    TASA_LLEGADA, TASA_POSICIONAMIENTO, TASA_DESPLIEGUE,
    CANTIDAD_ESTACIONES_CARGA, CANTIDAD_MONTACARGAS
)
from entidades import Vehiculo, EstadisticasOperacion


class Terminal:
    """Representa un centro logístico con estaciones de carga y montacargas"""
    
    def __init__(self, env):
        self.env = env
        self.estaciones_carga = simpy.Resource(env, capacity=CANTIDAD_ESTACIONES_CARGA)
        self.montacargas = simpy.Resource(env, capacity=CANTIDAD_MONTACARGAS)
        
        # Estadísticas
        self.estadisticas = EstadisticasOperacion()
        
        # Monitoreo de utilización
        self.tiempo_amarraderos_ocupados = 0
        self.tiempo_grua_ocupada = 0
        self.ultima_medicion = 0
    
    def actualizar_utilizacion(self, tiempo_actual):
        """Actualiza los contadores de utilización"""
        delta = tiempo_actual - self.ultima_medicion
        if delta > 0:
            self.tiempo_amarraderos_ocupados += self.estaciones_carga.count * delta
            self.tiempo_grua_ocupada += self.montacargas.count * delta
        self.ultima_medicion = tiempo_actual


def proceso_vehiculo(env, terminal, vehiculo):
    """
    Proceso que maneja el ciclo completo del vehículo.
    El montacargas se libera después de cada asistencia.
    """
    
    print(f"[{env.now:.2f}] VEHÍCULO LLEGÓ {vehiculo}")
    
    # ========== PASO 1: Solicitar estación de carga ==========
    with terminal.estaciones_carga.request() as req_estacion:
        # Esperar hasta que haya una estación de carga disponible
        yield req_estacion
        
        terminal.actualizar_utilizacion(env.now)
        print(f"[{env.now:.2f}] {vehiculo} obtuvo una estación de carga")
        
        # ========== PASO 2: Solicitar montacargas para POSICIONAMIENTO ==========
        with terminal.montacargas.request() as req_montacargas_entrada:
            yield req_montacargas_entrada
            
            terminal.actualizar_utilizacion(env.now)
            vehiculo.momento_inicio_posicionamiento = env.now
            
            # Calcular tiempo de espera (desde llegada hasta obtener grúa)
            tiempo_espera = env.now - vehiculo.momento_llegada
            vehiculo.momento_inicio_operacion = env.now  # La operación empieza después de posicionar
            
            print(f"[{env.now:.2f}] {vehiculo} obtuvo montacargas (posicionamiento) - Esperó {tiempo_espera:.2f}h")
            
            # Asistencia de posicionamiento (montacargas prepara el vehículo en la estación)
            tiempo_posicionamiento = random.expovariate(TASA_POSICIONAMIENTO)
            yield env.timeout(tiempo_posicionamiento)
            
            vehiculo.momento_fin_posicionamiento = env.now
            print(f"[{env.now:.2f}] {vehiculo} posicionamiento completado ({tiempo_posicionamiento:.2f}h)")
        
        # La grúa se LIBERA automáticamente al salir del with
        print(f"[{env.now:.2f}] {vehiculo} montacargas liberado (posicionamiento completado)")
        
        # ========== PASO 3: OPERACIÓN (el vehículo está en la estación de carga, sin montacargas) ==========
        vehiculo.estado = "operando"
        print(f"[{env.now:.2f}] {vehiculo} inicia operación ({vehiculo.tiempo_operacion:.2f}h)")
        yield env.timeout(vehiculo.tiempo_operacion)
        
        vehiculo.momento_fin_operacion = env.now
        vehiculo.estado = "operacion_completada"
        print(f"[{env.now:.2f}] {vehiculo} terminó operación")
        
        # ========== PASO 4: Solicitar montacargas para RETIRADA ==========
        with terminal.montacargas.request() as req_montacargas_salida:
            yield req_montacargas_salida
            
            terminal.actualizar_utilizacion(env.now)
            vehiculo.momento_inicio_despliegue = env.now
            
            tiempo_espera_despliegue = env.now - vehiculo.momento_fin_operacion
            print(f"[{env.now:.2f}] {vehiculo} obtuvo montacargas (retirada) - Esperó {tiempo_espera_despliegue:.2f}h para retirar")
            
            # Asistencia de despliegue
            tiempo_despliegue = random.expovariate(TASA_DESPLIEGUE)
            yield env.timeout(tiempo_despliegue)
            
            vehiculo.momento_fin_despliegue = env.now
            print(f"[{env.now:.2f}] {vehiculo} retirada completada ({tiempo_despliegue:.2f}h)")
        
        # La grúa se LIBERA nuevamente
        print(f"[{env.now:.2f}] {vehiculo} montacargas liberado (retirada completada)")
        
        # El amarradero se libera automáticamente al salir del with externo
        print(f"[{env.now:.2f}] {vehiculo} estación de carga liberada")
    
    # ========== REGISTRAR ESTADÍSTICAS ==========
    vehiculo.estado = "finalizado"
    terminal.estadisticas.registrar_vehiculo(vehiculo)
    
    print(f"[{env.now:.2f}] {vehiculo} - ESPERA: {vehiculo.tiempo_espera:.2f}h, SISTEMA: {vehiculo.tiempo_total_sistema:.2f}h")
    print("-" * 70)


def generador_vehiculos(env, terminal):
    """Genera vehículos según distribución exponencial"""
    while True:
        tiempo_entre_llegadas = random.expovariate(TASA_LLEGADA)
        yield env.timeout(tiempo_entre_llegadas)
        
        vehiculo = Vehiculo(env.now)
        env.process(proceso_vehiculo(env, terminal, vehiculo))


def ejecutar_simulacion(duracion_horas, semilla=None):
    """
    Ejecuta una simulación completa de la terminal.
    
    Args:
        duracion_horas: Duración de la simulación en horas
        semilla: Semilla para el generador aleatorio (opcional)
    
    Returns:
        EstadisticasOperacion: Objeto con todas las estadísticas
    """
    if semilla is not None:
        random.seed(semilla)
    
    # Crear entorno y terminal
    env = simpy.Environment()
    terminal = Terminal(env)
    
    # Iniciar generador de vehículos
    env.process(generador_vehiculos(env, terminal))
    
    # Ejecutar simulación
    env.run(until=duracion_horas)
    
    # Registrar utilización final
    terminal.actualizar_utilizacion(duracion_horas)
    
    # Calcular utilizaciones promedio
    if duracion_horas > 0:
        terminal.estadisticas.utilizacion_estaciones = terminal.tiempo_amarraderos_ocupados / (CANTIDAD_ESTACIONES_CARGA * duracion_horas)
        terminal.estadisticas.utilizacion_grua = terminal.tiempo_grua_ocupada / duracion_horas
    
    return terminal.estadisticas
