"""
Módulo de Aproximación de Series de Taylor

Este módulo proporciona funcionalidad para calcular aproximaciones de series de Taylor
y sus errores de truncamiento para funciones arbitrarias.
"""

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from sympy.utilities.lambdify import lambdify
from typing import Callable, Tuple, List, Union, Dict
import time
import os
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

# Función auxiliar para cálculo en paralelo
def _calcular_termino_paralelo(args):
    """
    Función auxiliar para calcular un término de Taylor en paralelo.
    
    Args:
        args: Tupla con (orden, x0, func_str)
        
    Returns:
        Tupla (orden, término)
    """
    orden, x0, func_str = args
    x = sp.Symbol('x')
    func = sp.sympify(func_str)
    
    if orden == 0:
        derivada = func
    else:
        derivada = sp.diff(func, x, orden)
    
    derivada_en_x0 = derivada.subs(x, x0)
    termino = derivada_en_x0 * (x - x0)**orden / sp.factorial(orden)
    
    return orden, termino

class AproximacionTaylor:
    """
    Una clase para calcular aproximaciones de series de Taylor y errores de truncamiento.
    """
    
    def __init__(self):
        """Inicializa la clase AproximacionTaylor."""
        self.x = sp.Symbol('x')
        self.cache = {}  # Caché para almacenar derivadas calculadas
        
    def establecer_funcion(self, func_str: str) -> None:
        """
        Establece la función a aproximar.
        
        Args:
            func_str: Una representación en cadena de la función en términos de x.
        """
        try:
            self.func = sp.sympify(func_str)
            self.func_str = func_str
            # Limpiar caché al establecer una nueva función
            self.cache = {}
        except Exception as e:
            raise ValueError(f"Expresión de función inválida: {e}")
    
    def derivar_funcion(self, orden: int) -> sp.Expr:
        """
        Calcula la derivada n-ésima de la función.
        
        Args:
            orden: El orden de la derivada.
            
        Returns:
            La expresión simbólica para la derivada n-ésima.
        """
        if orden in self.cache:
            return self.cache[orden]
        
        if orden == 0:
            result = self.func
        else:
            result = sp.diff(self.func, self.x, orden)
        
        # Almacenar el resultado en caché
        self.cache[orden] = result
        return result
    
    def analizar_termino_taylor(self, orden: int, x0: float) -> sp.Expr:
        """
        Calcula un solo término de la serie de Taylor.
        
        Args:
            orden: El orden del término.
            x0: El punto alrededor del cual expandir.
            
        Returns:
            La expresión simbólica para el término.
        """
        if orden == 0:
            return self.derivar_funcion(0).subs(self.x, x0)
        
        derivada = self.derivar_funcion(orden)
        derivada_en_x0 = derivada.subs(self.x, x0)
        
        return derivada_en_x0 * (self.x - x0)**orden / sp.factorial(orden)
    
    def visualizar_serie_taylor(self, x0: float, orden: int) -> sp.Expr:
        """
        Calcula la aproximación de la serie de Taylor hasta el orden especificado.
        
        Args:
            x0: El punto alrededor del cual expandir.
            orden: El orden máximo de la aproximación.
            
        Returns:
            La expresión simbólica para la serie de Taylor.
        """
        if orden > 200:
            raise ValueError("El orden máximo es 200")
        
        terminos = [self.analizar_termino_taylor(i, x0) for i in range(orden + 1)]
        return sum(terminos)
    
    def integrar_error_taylor(self, x0: float, orden: int, x_val: float) -> float:
        """
        Calcula el error de truncamiento en un punto específico.
        
        Args:
            x0: El punto alrededor del cual expandir.
            orden: El orden de la aproximación.
            x_val: El punto en el que evaluar el error.
            
        Returns:
            El valor del error de truncamiento.
        """
        # Calcular el valor exacto
        func_exacta = lambdify(self.x, self.func, "numpy")
        valor_exacto = float(func_exacta(x_val))
        
        # Calcular la aproximación
        aprox = self.visualizar_serie_taylor(x0, orden)
        func_aprox = lambdify(self.x, aprox, "numpy")
        valor_aprox = float(func_aprox(x_val))
        
        return abs(valor_exacto - valor_aprox)
    
    def determinar_limite_error(self, x0: float, orden: int, x_val: float) -> float:
        """
        Calcula el límite teórico del error basado en el resto de Lagrange.
        
        Args:
            x0: El punto alrededor del cual expandir.
            orden: El orden de la aproximación.
            x_val: El punto en el que evaluar el límite del error.
            
        Returns:
            El límite teórico del error.
        """
        # El límite del error es |f^(n+1)(ξ)| * |x - x0|^(n+1) / (n+1)!
        # donde ξ es algún punto entre x0 y x
        # Usaremos una estimación conservadora encontrando el valor máximo de la derivada
        
        siguiente_derivada = self.derivar_funcion(orden + 1)
        
        # Crear una función numérica para el valor absoluto de la derivada
        abs_derivada = sp.Lambda(self.x, sp.Abs(siguiente_derivada))
        num_derivada = lambdify(self.x, abs_derivada(self.x), "numpy")
        
        # Muestrear puntos entre x0 y x_val
        if x0 != x_val:
            puntos_muestra = np.linspace(min(x0, x_val), max(x0, x_val), 100)
            max_derivada = max(num_derivada(puntos_muestra))
        else:
            max_derivada = abs(float(siguiente_derivada.subs(self.x, x0)))
        
        return max_derivada * abs(x_val - x0)**(orden + 1) / sp.factorial(orden + 1)
    
    def graficar_aproximaciones(self, x0: float, ordenes: List[int], rango_x: Tuple[float, float], 
                           puntos: int = 1000, ruta_guardar: str = None) -> None:
        """
        Grafica la función original y sus aproximaciones de Taylor.
        
        Args:
            x0: El punto alrededor del cual expandir.
            ordenes: Lista de órdenes de aproximación a graficar.
            rango_x: Tupla (min_x, max_x) que define el rango del eje x.
            puntos: Número de puntos a usar para graficar.
            ruta_guardar: Ruta para guardar la gráfica. Si es None, la gráfica se muestra.
        """
        x_vals = np.linspace(rango_x[0], rango_x[1], puntos)
        
        # Crear una función para evaluación numérica
        func_num = lambdify(self.x, self.func, "numpy")
        
        plt.figure(figsize=(12, 8))
        
        # Graficar la función original
        try:
            y_vals = func_num(x_vals)
            plt.plot(x_vals, y_vals, 'k-', linewidth=2, label=f'f(x) = {self.func_str}')
        except Exception as e:
            print(f"Error al graficar la función original: {e}")
        
        # Graficar las aproximaciones
        colors = plt.cm.viridis(np.linspace(0, 1, len(ordenes)))
        
        for i, orden in enumerate(ordenes):
            aprox = self.visualizar_serie_taylor(x0, orden)
            aprox_num = lambdify(self.x, aprox, "numpy")
            
            try:
                y_aprox = aprox_num(x_vals)
                plt.plot(x_vals, y_aprox, '-', color=colors[i], linewidth=1.5, 
                         label=f'Orden {orden}')
            except Exception as e:
                print(f"Error al graficar la aproximación de orden {orden}: {e}")
        
        # Marcar el punto de expansión
        plt.axvline(x=x0, color='gray', linestyle='--', alpha=0.5)
        plt.scatter([x0], [func_num(x0)], color='red', s=50, zorder=5)
        plt.annotate(f'x₀ = {x0}', (x0, func_num(x0)), xytext=(10, -20), 
                    textcoords='offset points', color='red')
        
        plt.grid(True, alpha=0.3)
        plt.legend(loc='best')
        plt.title(f'Aproximaciones de Series de Taylor de f(x) = {self.func_str} alrededor de x₀ = {x0}')
        plt.xlabel('x')
        plt.ylabel('y')
        
        if ruta_guardar:
            plt.savefig(ruta_guardar, dpi=300, bbox_inches='tight')
            print(f"Gráfica guardada en {ruta_guardar}")
        else:
            plt.tight_layout()
            plt.show()
    
    def graficar_errores(self, x0: float, ordenes: List[int], rango_x: Tuple[float, float], 
                   puntos: int = 1000, escala_log: bool = True, ruta_guardar: str = None) -> None:
        """
        Grafica los errores de truncamiento para diferentes órdenes de aproximación.
        
        Args:
            x0: El punto alrededor del cual expandir.
            ordenes: Lista de órdenes de aproximación a graficar.
            rango_x: Tupla (min_x, max_x) que define el rango del eje x.
            puntos: Número de puntos a usar para graficar.
            escala_log: Si se debe usar escala logarítmica para el eje y.
            ruta_guardar: Ruta para guardar la gráfica. Si es None, la gráfica se muestra.
        """
        x_vals = np.linspace(rango_x[0], rango_x[1], puntos)
        
        plt.figure(figsize=(12, 8))
        
        # Crear una función para evaluación numérica
        func_num = lambdify(self.x, self.func, "numpy")
        
        # Calcular y graficar errores para cada orden
        colors = plt.cm.viridis(np.linspace(0, 1, len(ordenes)))
        
        for i, orden in enumerate(ordenes):
            aprox = self.visualizar_serie_taylor(x0, orden)
            aprox_num = lambdify(self.x, aprox, "numpy")
            
            try:
                # Calcular errores
                y_vals = func_num(x_vals)
                y_aprox = aprox_num(x_vals)
                errores = np.abs(y_vals - y_aprox)
                
                plt.plot(x_vals, errores, '-', color=colors[i], linewidth=1.5, 
                         label=f'Orden {orden}')
            except Exception as e:
                print(f"Error al graficar el error de orden {orden}: {e}")
        
        # Marcar el punto de expansión
        plt.axvline(x=x0, color='gray', linestyle='--', alpha=0.5)
        
        plt.grid(True, alpha=0.3)
        plt.legend(loc='best')
        plt.title(f'Errores de Truncamiento para Aproximaciones de Taylor de f(x) = {self.func_str}')
        plt.xlabel('x')
        plt.ylabel('Error (absoluto)')
        
        if escala_log:
            plt.yscale('log')
        
        if ruta_guardar:
            plt.savefig(ruta_guardar, dpi=300, bbox_inches='tight')
            print(f"Gráfica de error guardada en {ruta_guardar}")
        else:
            plt.tight_layout()
            plt.show()
    
    def calcular_terminos_taylor_paralelo(self, x0: float, orden_max: int, 
                                     num_procesos: int = None) -> Dict[int, sp.Expr]:
        """
        Calcula términos de la serie de Taylor en paralelo para mejor rendimiento.
        
        Args:
            x0: El punto alrededor del cual expandir.
            orden_max: El orden máximo a calcular.
            num_procesos: Número de procesos a usar. Si es None, usa el número de CPUs.
            
        Returns:
            Diccionario que mapea orden a expresiones de términos.
        """
        if orden_max > 200:
            raise ValueError("El orden máximo es 200")
        
        if num_procesos is None:
            num_procesos = multiprocessing.cpu_count()
        
        # Preparar los argumentos para la función paralela
        func_str = str(self.func)
        args_list = [(orden, x0, func_str) for orden in range(orden_max + 1)]
        
        terminos = {}
        with ProcessPoolExecutor(max_workers=num_procesos) as executor:
            for orden, termino in executor.map(_calcular_termino_paralelo, args_list):
                terminos[orden] = termino
        
        return terminos
    
    def exportar_aproximacion(self, x0: float, orden: int, nombre_archivo: str) -> None:
        """
        Exporta la aproximación de Taylor a un archivo.
        
        Args:
            x0: El punto alrededor del cual expandir.
            orden: El orden de la aproximación.
            nombre_archivo: El nombre del archivo para guardar la aproximación.
        """
        aprox = self.visualizar_serie_taylor(x0, orden)
        
        with open(nombre_archivo, 'w') as f:
            f.write(f"Función: {self.func_str}\n")
            f.write(f"Punto de expansión: x0 = {x0}\n")
            f.write(f"Orden: {orden}\n\n")
            f.write(f"Aproximación de Taylor:\n{aprox}\n\n")
            
            # También escribir la forma simplificada si es posible
            try:
                simplificado = sp.simplify(aprox)
                f.write(f"Forma simplificada:\n{simplificado}\n")
            except Exception as e:
                f.write(f"No se pudo simplificar: {e}\n")
        
        print(f"Aproximación exportada a {nombre_archivo}")
    
    def generar_informe(self, x0: float, ordenes: List[int], x_eval: List[float], 
                       directorio_salida: str = "resultados_taylor") -> None:
        """
        Genera un informe completo con aproximaciones y errores.
        
        Args:
            x0: El punto alrededor del cual expandir.
            ordenes: Lista de órdenes de aproximación a incluir.
            x_eval: Lista de valores x en los que evaluar la aproximación.
            directorio_salida: Directorio para guardar el informe y las gráficas.
        """
        # Crear directorio de salida si no existe
        os.makedirs(directorio_salida, exist_ok=True)
        
        # Generar archivo de informe
        archivo_informe = os.path.join(directorio_salida, "informe_taylor.txt")
        
        with open(archivo_informe, 'w') as f:
            f.write(f"INFORME DE APROXIMACIÓN DE SERIES DE TAYLOR\n")
            f.write(f"=========================================\n\n")
            f.write(f"Función: f(x) = {self.func_str}\n")
            f.write(f"Punto de expansión: x0 = {x0}\n\n")
            
            # Para cada orden, calcular e informar la aproximación
            for orden in ordenes:
                tiempo_inicio = time.time()
                aprox = self.visualizar_serie_taylor(x0, orden)
                tiempo_fin = time.time()
                
                f.write(f"\nAPROXIMACIÓN DE ORDEN {orden}\n")
                f.write(f"-------------------------\n")
                f.write(f"Tiempo de cálculo: {tiempo_fin - tiempo_inicio:.4f} segundos\n\n")
                
                # Escribir la aproximación
                f.write(f"Polinomio de Taylor:\n{aprox}\n\n")
                
                # Intentar simplificar
                try:
                    simplificado = sp.simplify(aprox)
                    f.write(f"Forma simplificada:\n{simplificado}\n\n")
                except Exception:
                    f.write("No se pudo simplificar la expresión.\n\n")
                
                # Evaluar en puntos específicos
                f.write("Evaluación en puntos específicos:\n")
                f.write("-" * 60 + "\n")
                f.write(f"{'x':^15} | {'Exacto':^15} | {'Aproximación':^15} | {'Error':^15}\n")
                f.write("-" * 60 + "\n")
                
                # Crear funciones numéricas
                func_num = lambdify(self.x, self.func, "numpy")
                aprox_num = lambdify(self.x, aprox, "numpy")
                
                for x_val in x_eval:
                    try:
                        exacto = func_num(x_val)
                        val_aprox = aprox_num(x_val)
                        error = abs(exacto - val_aprox)
                        
                        f.write(f"{x_val:15.6f} | {exacto:15.6f} | {val_aprox:15.6f} | {error:15.6e}\n")
                    except Exception as e:
                        f.write(f"{x_val:15.6f} | {'Error':^15} | {'Error':^15} | {'Error':^15} - {str(e)}\n")
                
                f.write("-" * 60 + "\n\n")
            
            # Generar gráficas
            f.write("\nGRÁFICAS\n")
            f.write("--------\n")
            f.write(f"Se han generado las siguientes gráficas en el directorio {directorio_salida}:\n")
            
            # Generar gráfica de aproximación
            ruta_aprox = os.path.join(directorio_salida, "aproximacion_taylor.png")
            self.graficar_aproximaciones(x0, ordenes, (min(x_eval), max(x_eval)), ruta_guardar=ruta_aprox)
            f.write(f"- Aproximación: {ruta_aprox}\n")
            
            # Generar gráfica de error
            ruta_error = os.path.join(directorio_salida, "error_taylor.png")
            self.graficar_errores(x0, ordenes, (min(x_eval), max(x_eval)), ruta_guardar=ruta_error)
            f.write(f"- Error: {ruta_error}\n")
        
        print(f"Informe generado en {archivo_informe}")
        return archivo_informe
