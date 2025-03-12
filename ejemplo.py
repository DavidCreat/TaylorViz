"""
Ejemplo de uso de la biblioteca de aproximación de series de Taylor.

Este script demuestra cómo usar la clase AproximacionTaylor para calcular
y visualizar aproximaciones de series de Taylor para diferentes funciones.
"""

from taylor_series import AproximacionTaylor
import numpy as np
import matplotlib.pyplot as plt
import os

def principal():
    # Crear una instancia de AproximacionTaylor
    taylor = AproximacionTaylor()
    
    # Definir la función a aproximar (en este caso, sin(x))
    taylor.establecer_funcion("sin(x)")
    
    # Punto de expansión
    x0 = 0
    
    # Diferentes órdenes para comparar
    ordenes = [1, 3, 5, 7]
    
    # Crear directorio para resultados
    directorio_salida = "resultados_ejemplo"
    os.makedirs(directorio_salida, exist_ok=True)
    
    # Generar aproximaciones y visualizaciones
    print(f"Generando aproximaciones de Taylor para f(x) = sin(x) alrededor de x0 = {x0}")
    
    # Evaluar en varios puntos
    puntos_evaluacion = [-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5]
    
    # Generar un informe completo
    archivo_informe = taylor.generar_informe(x0, ordenes, puntos_evaluacion, directorio_salida)
    
    print(f"\nInforme generado en: {archivo_informe}")
    print(f"Imágenes guardadas en: {directorio_salida}")
    
    # También podemos mostrar una gráfica interactiva
    print("\nMostrando gráfica interactiva...")
    taylor.graficar_aproximaciones(x0, ordenes, (-2, 2))
    
    print("\n¡Ejemplo completado!")

if __name__ == "__main__":
    principal()
