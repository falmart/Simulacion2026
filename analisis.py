import math
import numpy as np
from parametros import CANTIDAD_REPLICAS


def calcular_intervalo_confianza(datos, confianza=0.95):
    n = len(datos)
    if n == 0:
        return (0, 0, 0, 0)
    
    media = np.mean(datos)
    desviacion = np.std(datos, ddof=1)  # ddof=1 para desviación muestral
    
    # Valor crítico de t-student para n-1 grados de libertad
    from scipy import stats
    t_critico = stats.t.ppf((1 + confianza) / 2, n - 1)
    
    margen_error = t_critico * (desviacion / math.sqrt(n))
    
    return (media, margen_error, media - margen_error, media + margen_error)


def resumen_estadistico(resultados_replicas):
    tiempos_espera_promedio = [r.tiempo_espera_promedio for r in resultados_replicas if r.tiempos_espera]
    tiempos_sistema_promedio = [r.tiempo_sistema_promedio for r in resultados_replicas if r.tiempos_sistema]
    vehiculos_procesados = [r.total_vehiculos_procesados for r in resultados_replicas]
    utilizacion_estaciones = [r.utilizacion_estaciones for r in resultados_replicas if r.utilizacion_estaciones is not None]
    utilizacion_grua = [r.utilizacion_grua for r in resultados_replicas if r.utilizacion_grua is not None]
    
    resumen = {
        'num_replicas': len(resultados_replicas),
        'tiempo_espera': calcular_intervalo_confianza(tiempos_espera_promedio),
        'tiempo_sistema': calcular_intervalo_confianza(tiempos_sistema_promedio),
        'vehiculos_procesados': calcular_intervalo_confianza(vehiculos_procesados),
        'utilizacion_estaciones': calcular_intervalo_confianza(utilizacion_estaciones),
        'utilizacion_grua': calcular_intervalo_confianza(utilizacion_grua),
    }
    
    # Datos brutos para análisis adicional
    resumen['raw_tiempos_espera'] = tiempos_espera_promedio
    resumen['raw_vehiculos_procesados'] = vehiculos_procesados
    
    return resumen


def imprimir_resumen(resumen):
    print("\n" + "=" * 70)
    print("RESUMEN DE SIMULACIÓN - CENTRO LOGÍSTICO")
    print("=" * 70)
    
    print(f"\nRéplicas ejecutadas: {resumen['num_replicas']}")
    
    # Tiempo de espera
    media, error, inf, sup = resumen['tiempo_espera']
    print(f"\nTiempo promedio de ESPERA (llegada → inicio operación):")
    print(f"   Media: {media:.4f} horas ({media*60:.2f} minutos)")
    print(f"   Intervalo 95%: [{inf:.4f}, {sup:.4f}] horas")
    print(f"   Margen de error: ±{error:.4f} horas")
    
    # Tiempo en sistema
    media, error, inf, sup = resumen['tiempo_sistema']
    print(f"\nTiempo promedio en SISTEMA:")
    print(f"   Media: {media:.4f} horas ({media*60:.2f} minutos)")
    print(f"   Intervalo 95%: [{inf:.4f}, {sup:.4f}] horas")
    
    # Vehículos procesados
    media, error, inf, sup = resumen['vehiculos_procesados']
    print(f"\nVehículos procesados (promedio por simulación):")
    print(f"   Media: {media:.1f}")
    print(f"   Intervalo 95%: [{inf:.1f}, {sup:.1f}]")
    
    # Utilización de amarraderos
    if resumen['utilizacion_estaciones'][0] is not None:
        media, error, inf, sup = resumen['utilizacion_estaciones']
        print(f"\nUtilización promedio de estaciones de carga:")
        print(f"   Media: {media:.2%}")
        print(f"   Intervalo 95%: [{inf:.2%}, {sup:.2%}]")
    
    # Utilización de montacargas
    if resumen['utilizacion_grua'][0] is not None:
        media, error, inf, sup = resumen['utilizacion_grua']
        print(f"\nUtilización promedio de montacargas:")
        print(f"   Media: {media:.2%}")
        print(f"   Intervalo 95%: [{inf:.2%}, {sup:.2%}]")
    
    print("\n" + "=" * 70)
