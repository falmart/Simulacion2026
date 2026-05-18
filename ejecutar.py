from parametros import TIEMPO_SIMULACION_HORAS, CANTIDAD_REPLICAS
from terminal import ejecutar_simulacion
from analisis import resumen_estadistico, imprimir_resumen


def ejecutar_replicas(num_replicas, duracion_horas, semilla_base=42):
    resultados = []
    
    print(f"Iniciando {num_replicas} réplicas de simulación...")
    print(f"Duración de cada simulación: {duracion_horas} horas")
    print("-" * 50)
    
    for i in range(num_replicas):
        # Usar semilla diferente para cada réplica
        semilla = semilla_base + i
        print(f"Ejecutando réplica {i+1}/{num_replicas} (semilla={semilla})...")
        
        try:
            estadisticas = ejecutar_simulacion(duracion_horas, semilla)
            resultados.append(estadisticas)
            
            # Reporte breve de esta réplica
            if estadisticas.tiempos_espera:  # ← CORREGIDO: 'if' añadido
                print(f"  Completada: {estadisticas.total_vehiculos_procesados} vehículos, "
                      f"espera promedio={estadisticas.tiempo_espera_promedio:.2f}h")
            else:
                print(f"  Réplica sin vehículos procesados")
                
        except Exception as e:
            print(f"  ❌ Error en réplica {i+1}: {e}")
            continue
    
    print("-" * 50)
    print(f"Simulaciones completadas: {len(resultados)} réplicas exitosas")
    
    return resultados


def main():
    print("=" * 70)
    print("SIMULACIÓN DE EVENTOS DISCRETOS - CENTRO LOGÍSTICO")
    print("=" * 70)
    print(f"\nConfiguración:")
    print(f"  - Estaciones de carga: 3")
    print(f"  - Montacargas: 1")
    print(f"  - Tasa de llegada: 1 vehículo cada {1/0.125:.0f} horas")
    print(f"  - Duración por simulación: {TIEMPO_SIMULACION_HORAS} horas ({TIEMPO_SIMULACION_HORAS/24:.1f} días)")
    print(f"  - Número de réplicas: {CANTIDAD_REPLICAS}")
    
    # Ejecutar réplicas
    resultados = ejecutar_replicas(CANTIDAD_REPLICAS, TIEMPO_SIMULACION_HORAS)
    
    if not resultados:
        print("\nNo se obtuvieron resultados válidos.")
        return
    
    # Generar resumen estadístico
    resumen = resumen_estadistico(resultados)
    imprimir_resumen(resumen)
    
    # Guardar resultados en archivo (opcional)
    guardar_resultados(resumen, "resultados_simulacion.txt")
    
    print("\nSimulación completada exitosamente.")
    print("\nPara generar informe en PDF con LaTeX:")
    print("  python generar_informe.py")
    
    return resumen


def guardar_resultados(resumen, archivo):
    """
    Guarda los resultados en un archivo de texto.
    """
    try:
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("RESULTADOS DE SIMULACIÓN - TERMINAL PORTUARIA\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Número de réplicas: {resumen['num_replicas']}\n\n")
            
            # Tiempo de espera
            media, error, inf, sup = resumen['tiempo_espera']
            f.write("TIEMPO PROMEDIO DE ESPERA:\n")
            f.write(f"  Media: {media:.4f} horas\n")
            f.write(f"  Intervalo 95%: [{inf:.4f}, {sup:.4f}]\n\n")
            
            # Tiempo en sistema
            media, error, inf, sup = resumen['tiempo_sistema']
            f.write("TIEMPO PROMEDIO EN SISTEMA:\n")
            f.write(f"  Media: {media:.4f} horas\n")
            f.write(f"  Intervalo 95%: [{inf:.4f}, {sup:.4f}]\n\n")
            
            # Vehículos procesados (CORREGIDO: cambiado de 'embarcaciones_procesadas')
            media, error, inf, sup = resumen['vehiculos_procesados']
            f.write("VEHÍCULOS PROCESADOS:\n")
            f.write(f"  Media: {media:.1f}\n")
            f.write(f"  Intervalo 95%: [{inf:.1f}, {sup:.1f}]\n\n")
            
            # Datos brutos (CORREGIDO: cambiado de 'raw_embarcaciones_procesadas')
            f.write("DATOS BRUTOS POR RÉPLICA:\n")
            f.write("Réplica, Tiempo Espera Prom, Vehículos Procesados\n")
            for i, (te, ep) in enumerate(zip(resumen['raw_tiempos_espera'], resumen['raw_vehiculos_procesados'])):
                f.write(f"{i+1}, {te:.4f}, {ep}\n")
        
        print(f"\nResultados guardados en '{archivo}'")
    except Exception as e:
        print(f"\nNo se pudo guardar el archivo: {e}")


if __name__ == "__main__":
    main()