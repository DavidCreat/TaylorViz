"""
Herramienta de Aproximación de Series de Taylor

Este script proporciona una interfaz de línea de comandos para calcular aproximaciones
de series de Taylor y sus errores de truncamiento para funciones arbitrarias.
"""

import os
import sys
import argparse
import sympy as sp
from taylor_series import AproximacionTaylor
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple

def analizar_argumentos():
    """Analiza los argumentos de la línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Calcula aproximaciones de series de Taylor y errores de truncamiento."
    )
    
    parser.add_argument(
        "-f", "--funcion", 
        type=str, 
        required=True,
        help="Función a aproximar (en términos de x, usando sintaxis de SymPy)"
    )
    
    parser.add_argument(
        "-x0", "--punto-expansion", 
        type=float, 
        required=True,
        help="Punto alrededor del cual expandir la serie de Taylor"
    )
    
    parser.add_argument(
        "-o", "--orden", 
        type=int, 
        required=True,
        help="Orden de la aproximación de Taylor (máximo 200)"
    )
    
    parser.add_argument(
        "-e", "--evaluar", 
        type=float, 
        nargs="+",
        help="Puntos en los que evaluar la aproximación"
    )
    
    parser.add_argument(
        "-p", "--graficar", 
        action="store_true",
        help="Generar gráficas de la aproximación y errores"
    )
    
    parser.add_argument(
        "-r", "--rango", 
        type=float, 
        nargs=2,
        metavar=("MIN", "MAX"),
        help="Rango para graficar (min_x max_x)"
    )
    
    parser.add_argument(
        "-c", "--comparar", 
        type=int, 
        nargs="+",
        help="Comparar múltiples órdenes de aproximación"
    )
    
    parser.add_argument(
        "-s", "--guardar", 
        type=str,
        help="Guardar resultados en el directorio especificado"
    )
    
    parser.add_argument(
        "--paralelo", 
        action="store_true",
        help="Usar cálculo en paralelo para mejor rendimiento"
    )
    
    return parser.parse_args()

def validar_args(args):
    """Valida los argumentos de la línea de comandos."""
    if args.orden < 0 or args.orden > 200:
        print("Error: El orden debe estar entre 0 y 200.")
        sys.exit(1)
    
    if args.comparar:
        for orden in args.comparar:
            if orden < 0 or orden > 200:
                print(f"Error: Orden inválido {orden} en --comparar. Los órdenes deben estar entre 0 y 200.")
                sys.exit(1)
    
    if args.graficar and not args.rango:
        print("Advertencia: No se especificó rango para graficar. Usando rango predeterminado.")

def imprimir_encabezado():
    """Imprime un encabezado para la aplicación."""
    print("\n" + "=" * 80)
    print(" " * 20 + "HERRAMIENTA DE APROXIMACIÓN DE SERIES DE TAYLOR")
    print("=" * 80 + "\n")

def imprimir_info_funcion(taylor, x0, orden):
    """Imprime información sobre la función y configuración de aproximación."""
    print(f"Función: f(x) = {taylor.func_str}")
    print(f"Punto de expansión: x0 = {x0}")
    print(f"Orden de aproximación: {orden}")
    print("-" * 80)

def imprimir_aproximacion(taylor, x0, orden):
    """Imprime la aproximación de la serie de Taylor."""
    print("\nAproximación de Serie de Taylor:")
    
    # Calcular la aproximación
    aprox = taylor.visualizar_serie_taylor(x0, orden)
    print(f"\n{aprox}\n")
    
    # Intentar simplificar
    try:
        simplificado = sp.simplify(aprox)
        print("Forma simplificada:")
        print(f"{simplificado}\n")
    except Exception as e:
        print(f"No se pudo simplificar: {e}\n")

def evaluar_en_puntos(taylor, x0, orden, puntos):
    """Evalúa la aproximación en puntos específicos."""
    if not puntos:
        return
    
    print("\nEvaluación en puntos específicos:")
    print("-" * 80)
    print(f"{'x':^15} | {'Exacto':^15} | {'Aproximación':^15} | {'Error':^15} | {'Límite Error':^15}")
    print("-" * 80)
    
    # Calcular la aproximación
    aprox = taylor.visualizar_serie_taylor(x0, orden)
    
    # Crear funciones numéricas
    x = sp.Symbol('x')
    func_num = sp.lambdify(x, taylor.func, "numpy")
    aprox_num = sp.lambdify(x, aprox, "numpy")
    
    for punto in puntos:
        try:
            exacto = func_num(punto)
            val_aprox = aprox_num(punto)
            error = abs(exacto - val_aprox)
            
            # Calcular límite de error
            limite_error = taylor.determinar_limite_error(x0, orden, punto)
            
            print(f"{punto:15.6f} | {exacto:15.6f} | {val_aprox:15.6f} | {error:15.6e} | {limite_error:15.6e}")
        except Exception as e:
            print(f"{punto:15.6f} | {'Error':^15} | {'Error':^15} | {'Error':^15} | {'Error':^15} - {str(e)}")
    
    print("-" * 80)

def generar_graficas(taylor, x0, ordenes, rango_x, dir_guardar=None):
    """Genera gráficas para la aproximación y errores."""
    if not rango_x:
        # Rango predeterminado: x0 ± 2
        rango_x = (x0 - 2, x0 + 2)
    
    # Asegurar que el directorio existe si se está guardando
    if dir_guardar:
        os.makedirs(dir_guardar, exist_ok=True)
    
    # Graficar aproximaciones
    print("\nGenerando gráfica de aproximación...")
    ruta_aprox = os.path.join(dir_guardar, "aproximacion_taylor.png") if dir_guardar else None
    taylor.graficar_aproximaciones(x0, ordenes, rango_x, ruta_guardar=ruta_aprox)
    
    # Graficar errores
    print("Generando gráfica de error...")
    ruta_error = os.path.join(dir_guardar, "error_taylor.png") if dir_guardar else None
    taylor.graficar_errores(x0, ordenes, rango_x, ruta_guardar=ruta_error)
    
    if dir_guardar:
        print(f"Gráficas guardadas en {dir_guardar}")

def main():
    """Función principal para ejecutar la herramienta de aproximación de series de Taylor."""
    # Configurar la codificación de salida para manejar caracteres Unicode
    try:
        # Intentar configurar la codificación de la consola a UTF-8
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    except Exception:
        # Si falla, continuamos con la configuración predeterminada
        pass
    
    # Analizar y validar argumentos
    args = analizar_argumentos()
    validar_args(args)
    
    # Imprimir encabezado
    imprimir_encabezado()
    
    # Crear objeto de aproximación de Taylor
    taylor = AproximacionTaylor()
    
    try:
        # Establecer la función
        taylor.establecer_funcion(args.funcion)
        
        # Obtener parámetros
        x0 = args.punto_expansion
        orden = args.orden
        
        # Imprimir información de la función
        imprimir_info_funcion(taylor, x0, orden)
        
        # Calcular e imprimir la aproximación
        if args.paralelo:
            print("Usando cálculo en paralelo...")
            try:
                terminos = taylor.calcular_terminos_taylor_paralelo(x0, orden)
                # Sumar los términos para obtener la aproximación
                aprox = sum(terminos.values())
                print("\nAproximación de Serie de Taylor (calculada en paralelo):")
                print(f"\n{aprox}\n")
                
                # Intentar simplificar
                try:
                    simplificado = sp.simplify(aprox)
                    print("Forma simplificada:")
                    print(f"{simplificado}\n")
                except Exception as e:
                    print(f"No se pudo simplificar: {e}\n")
            except Exception as e:
                print(f"Error en el cálculo paralelo: {e}")
                print("Continuando con cálculo secuencial...")
                imprimir_aproximacion(taylor, x0, orden)
        else:
            imprimir_aproximacion(taylor, x0, orden)
        
        # Evaluar en puntos específicos si se solicita
        if args.evaluar:
            evaluar_en_puntos(taylor, x0, orden, args.evaluar)
        
        # Generar gráficas si se solicita
        if args.graficar:
            ordenes_a_graficar = [orden]
            if args.comparar:
                ordenes_a_graficar = sorted(set(ordenes_a_graficar + args.comparar))
            
            generar_graficas(taylor, x0, ordenes_a_graficar, args.rango, args.guardar)
        
        # Generar un informe completo si se especifica directorio para guardar
        if args.guardar and args.evaluar:
            print(f"\nGenerando informe completo en {args.guardar}...")
            
            ordenes_a_informar = [orden]
            if args.comparar:
                ordenes_a_informar = sorted(set(ordenes_a_informar + args.comparar))
            
            archivo_informe = taylor.generar_informe(x0, ordenes_a_informar, args.evaluar, args.guardar)
            print(f"Informe generado: {archivo_informe}")
        
        print("\n¡Aproximación de serie de Taylor completada exitosamente!")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
