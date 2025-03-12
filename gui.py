"""
Interfaz Gráfica para la Herramienta de Aproximación de Series de Taylor

Este script proporciona una interfaz gráfica de usuario para la herramienta de aproximación
de series de Taylor, facilitando la visualización e interacción con las aproximaciones.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import sympy as sp
import os
import threading
import time
from taylor_series import AproximacionTaylor

class InterfazTaylor:
    """Interfaz Gráfica para la Herramienta de Aproximación de Series de Taylor."""
    
    def __init__(self, root):
        """Inicializar la interfaz gráfica."""
        self.root = root
        self.root.title("Aproximaciones de Taylor")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Establecer tema
        style = ttk.Style()
        style.theme_use('clam')  # Usar un tema moderno
        
        # Crear objeto de aproximación de Taylor
        self.taylor = AproximacionTaylor()
        
        # Valores predeterminados
        self.funcion_predeterminada = "sin(x)"
        self.x0_predeterminado = 0
        self.orden_predeterminado = 5
        self.rango_predeterminado = (-2, 2)
        
        # Crear marco principal
        self.marco_principal = ttk.Frame(self.root)
        self.marco_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear panel izquierdo para entradas
        self.panel_izquierdo = ttk.Frame(self.marco_principal, width=300)
        self.panel_izquierdo.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Crear panel derecho para gráficas
        self.panel_derecho = ttk.Frame(self.marco_principal)
        self.panel_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Crear widgets de entrada
        self.crear_widgets_entrada()
        
        # Crear área de gráficas
        self.crear_area_graficas()
        
        # Crear barra de estado
        self.var_estado = tk.StringVar()
        self.var_estado.set("Listo")
        self.barra_estado = ttk.Label(self.root, textvariable=self.var_estado, relief=tk.SUNKEN, anchor=tk.W)
        self.barra_estado.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Establecer función predeterminada
        self.entrada_funcion.insert(0, self.funcion_predeterminada)
        self.entrada_x0.insert(0, str(self.x0_predeterminado))
        self.spinbox_orden.set(str(self.orden_predeterminado))
        self.entrada_x_min.insert(0, str(self.rango_predeterminado[0]))
        self.entrada_x_max.insert(0, str(self.rango_predeterminado[1]))
        
        # Inicializar con función predeterminada
        self.actualizar_funcion()
    
    def crear_widgets_entrada(self):
        """Crear widgets de entrada en el panel izquierdo."""
        # Entrada de función
        ttk.Label(self.panel_izquierdo, text="Función f(x):", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.entrada_funcion = ttk.Entry(self.panel_izquierdo, width=30)
        self.entrada_funcion.grid(row=1, column=0, sticky=tk.W+tk.E, pady=(0, 10))
        
        # Ejemplos de funciones
        ttk.Label(self.panel_izquierdo, text="Ejemplos:").grid(row=2, column=0, sticky=tk.W)
        marco_ejemplos = ttk.Frame(self.panel_izquierdo)
        marco_ejemplos.grid(row=3, column=0, sticky=tk.W+tk.E, pady=(0, 10))
        
        funciones_ejemplo = [
            "sin(x)", "cos(x)", "exp(x)", "log(x)", 
            "tan(x)", "x**2", "1/x", "sqrt(x)"
        ]
        
        for i, func in enumerate(funciones_ejemplo):
            btn = ttk.Button(marco_ejemplos, text=func, width=8,
                            command=lambda f=func: self.establecer_funcion_ejemplo(f))
            btn.grid(row=i//4, column=i%4, padx=2, pady=2)
        
        # Punto de expansión
        ttk.Label(self.panel_izquierdo, text="Punto de expansión (x₀):").grid(row=4, column=0, sticky=tk.W, pady=(10, 5))
        self.entrada_x0 = ttk.Entry(self.panel_izquierdo, width=10)
        self.entrada_x0.grid(row=5, column=0, sticky=tk.W, pady=(0, 10))
        
        # Orden
        ttk.Label(self.panel_izquierdo, text="Orden de aproximación:").grid(row=6, column=0, sticky=tk.W, pady=(0, 5))
        marco_orden = ttk.Frame(self.panel_izquierdo)
        marco_orden.grid(row=7, column=0, sticky=tk.W, pady=(0, 10))
        
        self.spinbox_orden = ttk.Spinbox(marco_orden, from_=1, to=200, width=5)
        self.spinbox_orden.pack(side=tk.LEFT)
        
        # Comparar órdenes
        ttk.Label(self.panel_izquierdo, text="Comparar órdenes:").grid(row=8, column=0, sticky=tk.W, pady=(0, 5))
        self.var_comparar = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.panel_izquierdo, text="Mostrar múltiples órdenes", 
                       variable=self.var_comparar).grid(row=9, column=0, sticky=tk.W)
        
        marco_comparar = ttk.Frame(self.panel_izquierdo)
        marco_comparar.grid(row=10, column=0, sticky=tk.W+tk.E, pady=(5, 10))
        
        self.ordenes_comparar = []
        for i in range(5):
            var = tk.BooleanVar(value=(i < 3))  # Primeros 3 marcados por defecto
            chk = ttk.Checkbutton(marco_comparar, text=str((i+1)*2), variable=var)
            chk.grid(row=0, column=i, padx=5)
            self.ordenes_comparar.append((var, (i+1)*2))
        
        # Rango de visualización
        ttk.Label(self.panel_izquierdo, text="Rango de visualización:").grid(row=11, column=0, sticky=tk.W, pady=(10, 5))
        marco_rango = ttk.Frame(self.panel_izquierdo)
        marco_rango.grid(row=12, column=0, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(marco_rango, text="Min:").pack(side=tk.LEFT)
        self.entrada_x_min = ttk.Entry(marco_rango, width=5)
        self.entrada_x_min.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(marco_rango, text="Max:").pack(side=tk.LEFT)
        self.entrada_x_max = ttk.Entry(marco_rango, width=5)
        self.entrada_x_max.pack(side=tk.LEFT)
        
        # Puntos de evaluación
        ttk.Label(self.panel_izquierdo, text="Puntos de evaluación (separados por comas):").grid(row=13, column=0, sticky=tk.W, pady=(10, 5))
        self.entrada_puntos_eval = ttk.Entry(self.panel_izquierdo)
        self.entrada_puntos_eval.grid(row=14, column=0, sticky=tk.W+tk.E, pady=(0, 10))
        self.entrada_puntos_eval.insert(0, "-1, -0.5, 0, 0.5, 1")
        
        # Botones
        marco_botones = ttk.Frame(self.panel_izquierdo)
        marco_botones.grid(row=15, column=0, sticky=tk.W+tk.E, pady=(10, 0))
        
        ttk.Button(marco_botones, text="Actualizar", command=self.actualizar_funcion).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(marco_botones, text="Evaluar", command=self.evaluar_puntos).pack(side=tk.LEFT, padx=5)
        ttk.Button(marco_botones, text="Guardar Informe", command=self.guardar_informe).pack(side=tk.LEFT, padx=5)
        
        # Añadir un separador
        ttk.Separator(self.panel_izquierdo, orient=tk.HORIZONTAL).grid(row=16, column=0, sticky=tk.W+tk.E, pady=10)
        
        # Área de resultados
        ttk.Label(self.panel_izquierdo, text="Resultados:", font=("Arial", 10, "bold")).grid(row=17, column=0, sticky=tk.W, pady=(0, 5))
        
        self.texto_resultados = tk.Text(self.panel_izquierdo, width=40, height=15, wrap=tk.WORD)
        self.texto_resultados.grid(row=18, column=0, sticky=tk.W+tk.E+tk.N+tk.S, pady=(0, 10))
        
        # Añadir barra de desplazamiento a resultados
        barra_resultados = ttk.Scrollbar(self.panel_izquierdo, command=self.texto_resultados.yview)
        barra_resultados.grid(row=18, column=1, sticky=tk.N+tk.S)
        self.texto_resultados.config(yscrollcommand=barra_resultados.set)
        
        # Hacer que el área de resultados sea expandible
        self.panel_izquierdo.grid_rowconfigure(18, weight=1)
        self.panel_izquierdo.grid_columnconfigure(0, weight=1)
    
    def crear_area_graficas(self):
        """Crear el área de gráficas en el panel derecho."""
        # Crear notebook para diferentes gráficas
        self.notebook = ttk.Notebook(self.panel_derecho)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Gráfica de aproximación de Taylor
        self.marco_aprox = ttk.Frame(self.notebook)
        self.notebook.add(self.marco_aprox, text="Aproximación")
        
        # Gráfica de error
        self.marco_error = ttk.Frame(self.notebook)
        self.notebook.add(self.marco_error, text="Error")
        
        # Crear figuras iniciales
        self.crear_figuras()
    
    def crear_figuras(self):
        """Crear figuras de matplotlib para graficar."""
        # Figura de aproximación
        self.fig_aprox, self.ax_aprox = plt.subplots(figsize=(8, 6))
        self.canvas_aprox = FigureCanvasTkAgg(self.fig_aprox, master=self.marco_aprox)
        self.canvas_aprox.draw()
        self.canvas_aprox.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Añadir barra de herramientas
        self.barra_aprox = NavigationToolbar2Tk(self.canvas_aprox, self.marco_aprox)
        self.barra_aprox.update()
        
        # Figura de error
        self.fig_error, self.ax_error = plt.subplots(figsize=(8, 6))
        self.canvas_error = FigureCanvasTkAgg(self.fig_error, master=self.marco_error)
        self.canvas_error.draw()
        self.canvas_error.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Añadir barra de herramientas
        self.barra_error = NavigationToolbar2Tk(self.canvas_error, self.marco_error)
        self.barra_error.update()
    
    def establecer_funcion_ejemplo(self, func):
        """Establecer una función de ejemplo en el campo de entrada."""
        self.entrada_funcion.delete(0, tk.END)
        self.entrada_funcion.insert(0, func)
        self.actualizar_funcion()
    
    def obtener_ordenes_seleccionados(self):
        """Obtener los órdenes seleccionados para comparación."""
        ordenes = []
        
        # Añadir el orden principal
        try:
            orden_principal = int(self.spinbox_orden.get())
            ordenes.append(orden_principal)
        except ValueError:
            pass
        
        # Añadir órdenes de comparación si está habilitado
        if self.var_comparar.get():
            for var, orden in self.ordenes_comparar:
                if var.get():
                    ordenes.append(orden)
        
        return sorted(set(ordenes))
    
    def obtener_rango_grafica(self):
        """Obtener el rango de visualización de los campos de entrada."""
        try:
            x_min = float(self.entrada_x_min.get())
            x_max = float(self.entrada_x_max.get())
            return (x_min, x_max)
        except ValueError:
            messagebox.showerror("Error", "Rango de visualización inválido")
            return self.rango_predeterminado
    
    def actualizar_funcion(self):
        """Actualizar la función y las gráficas."""
        # Obtener función y parámetros
        func_str = self.entrada_funcion.get()
        if not func_str:
            messagebox.showerror("Error", "Por favor ingrese una función")
            return
        
        try:
            x0 = float(self.entrada_x0.get())
        except ValueError:
            messagebox.showerror("Error", "Punto de expansión inválido")
            return
        
        # Actualizar estado
        self.var_estado.set("Calculando aproximaciones...")
        self.root.update_idletasks()
        
        # Ejecutar el cálculo en un hilo separado para evitar congelar la interfaz
        threading.Thread(target=self.dibujar_aproximaciones, 
                         args=(func_str, x0)).start()
    
    def dibujar_aproximaciones(self, func_str, x0):
        """Función de hilo para actualizar la función y las gráficas."""
        try:
            # Establecer la función
            self.taylor.establecer_funcion(func_str)
            
            # Obtener órdenes y rango
            ordenes = self.obtener_ordenes_seleccionados()
            rango_x = self.obtener_rango_grafica()
            
            # Actualizar gráficas
            self.actualizar_graficas(x0, ordenes, rango_x)
            
            # Actualizar texto de resultados
            self.actualizar_resultados(x0, ordenes[0])
            
            # Actualizar estado
            self.var_estado.set(f"Función actualizada: f(x) = {func_str}")
        
        except Exception as e:
            # Manejar errores
            mensaje_error = str(e)
            self.var_estado.set(f"Error: {mensaje_error}")
            messagebox.showerror("Error", mensaje_error)
    
    def actualizar_graficas(self, x0, ordenes, rango_x):
        """Actualizar las gráficas con nueva función y parámetros."""
        # Limpiar gráficas anteriores
        self.ax_aprox.clear()
        self.ax_error.clear()
        
        # Graficar aproximaciones
        x_vals = np.linspace(rango_x[0], rango_x[1], 1000)
        
        # Crear una función para evaluación numérica
        x = sp.Symbol('x')
        func_num = sp.lambdify(x, self.taylor.func, "numpy")
        
        # Graficar la función original
        try:
            y_vals = func_num(x_vals)
            self.ax_aprox.plot(x_vals, y_vals, 'k-', linewidth=2, label=f'f(x) = {self.taylor.func_str}')
        except Exception as e:
            print(f"Error al graficar la función original: {e}")
        
        # Graficar las aproximaciones
        colores = plt.cm.viridis(np.linspace(0, 1, len(ordenes)))
        
        for i, orden in enumerate(ordenes):
            aprox = self.taylor.visualizar_serie_taylor(x0, orden)
            aprox_num = sp.lambdify(x, aprox, "numpy")
            
            try:
                y_aprox = aprox_num(x_vals)
                self.ax_aprox.plot(x_vals, y_aprox, '-', color=colores[i], linewidth=1.5, 
                                  label=f'Orden {orden}')
                
                # Graficar errores
                errores = np.abs(y_vals - y_aprox)
                self.ax_error.plot(x_vals, errores, '-', color=colores[i], linewidth=1.5, 
                                 label=f'Orden {orden}')
            except Exception as e:
                print(f"Error al graficar la aproximación de orden {orden}: {e}")
        
        # Marcar el punto de expansión
        self.ax_aprox.axvline(x=x0, color='gray', linestyle='--', alpha=0.5)
        self.ax_aprox.scatter([x0], [func_num(x0)], color='red', s=50, zorder=5)
        self.ax_aprox.annotate(f'x₀ = {x0}', (x0, func_num(x0)), xytext=(10, -20), 
                              textcoords='offset points', color='red')
        
        # Establecer propiedades de la gráfica
        self.ax_aprox.grid(True, alpha=0.3)
        self.ax_aprox.legend(loc='best')
        self.ax_aprox.set_title(f'Aproximaciones de Taylor para f(x) = {self.taylor.func_str}')
        self.ax_aprox.set_xlabel('x')
        self.ax_aprox.set_ylabel('y')
        
        # Establecer propiedades de la gráfica de error
        self.ax_error.grid(True, alpha=0.3)
        self.ax_error.legend(loc='best')
        self.ax_error.set_title(f'Errores de truncamiento')
        self.ax_error.set_xlabel('x')
        self.ax_error.set_ylabel('Error (absoluto)')
        self.ax_error.set_yscale('log')
        
        # Marcar el punto de expansión en la gráfica de error
        self.ax_error.axvline(x=x0, color='gray', linestyle='--', alpha=0.5)
        
        # Actualizar lienzos
        self.canvas_aprox.draw()
        self.canvas_error.draw()
    
    def actualizar_resultados(self, x0, orden):
        """Actualizar el área de texto de resultados con información de aproximación."""
        # Limpiar resultados anteriores
        self.texto_resultados.delete(1.0, tk.END)
        
        # Calcular la aproximación
        aprox = self.taylor.visualizar_serie_taylor(x0, orden)
        
        # Mostrar información de la función
        self.texto_resultados.insert(tk.END, f"Función: f(x) = {self.taylor.func_str}\n\n")
        self.texto_resultados.insert(tk.END, f"Punto de expansión: x₀ = {x0}\n\n")
        self.texto_resultados.insert(tk.END, f"Orden de aproximación: {orden}\n\n")
        
        # Mostrar la aproximación
        self.texto_resultados.insert(tk.END, "Polinomio de Taylor:\n")
        self.texto_resultados.insert(tk.END, f"{aprox}\n\n")
        
        # Intentar simplificar
        try:
            simplificado = sp.simplify(aprox)
            self.texto_resultados.insert(tk.END, "Forma simplificada:\n")
            self.texto_resultados.insert(tk.END, f"{simplificado}\n\n")
        except Exception:
            pass
    
    def evaluar_puntos(self):
        """Evaluar la aproximación en puntos específicos."""
        # Obtener parámetros de la función
        try:
            x0 = float(self.entrada_x0.get())
            orden = int(self.spinbox_orden.get())
        except ValueError:
            messagebox.showerror("Error", "Parámetros inválidos")
            return
        
        # Obtener puntos de evaluación
        puntos_str = self.entrada_puntos_eval.get()
        try:
            puntos = [float(x.strip()) for x in puntos_str.split(",")]
        except ValueError:
            messagebox.showerror("Error", "Puntos de evaluación inválidos")
            return
        
        # Actualizar estado
        self.var_estado.set("Evaluando puntos...")
        self.root.update_idletasks()
        
        # Ejecutar evaluación en un hilo separado
        threading.Thread(target=self.ejecutar_evaluacion, 
                         args=(x0, orden, puntos)).start()
    
    def ejecutar_evaluacion(self, x0, orden, puntos):
        """Función de hilo para evaluar puntos."""
        try:
            # Calcular la aproximación
            aprox = self.taylor.visualizar_serie_taylor(x0, orden)
            
            # Crear funciones numéricas
            x = sp.Symbol('x')
            func_num = sp.lambdify(x, self.taylor.func, "numpy")
            aprox_num = sp.lambdify(x, aprox, "numpy")
            
            # Añadir resultados de evaluación al área de texto
            self.texto_resultados.insert(tk.END, "\nEvaluación en puntos específicos:\n")
            self.texto_resultados.insert(tk.END, "-" * 60 + "\n")
            self.texto_resultados.insert(tk.END, f"{'x':^10} | {'Exacto':^15} | {'Aproximación':^15} | {'Error':^15}\n")
            self.texto_resultados.insert(tk.END, "-" * 60 + "\n")
            
            for punto in puntos:
                try:
                    exacto = func_num(punto)
                    val_aprox = aprox_num(punto)
                    error = abs(exacto - val_aprox)
                    
                    self.texto_resultados.insert(tk.END, 
                                           f"{punto:10.4f} | {exacto:15.6f} | {val_aprox:15.6f} | {error:15.6e}\n")
                except Exception as e:
                    self.texto_resultados.insert(tk.END, 
                                           f"{punto:10.4f} | {'Error':^15} | {'Error':^15} | {'Error':^15} - {str(e)}\n")
            
            self.texto_resultados.insert(tk.END, "-" * 60 + "\n")
            
            # Actualizar estado
            self.var_estado.set(f"Evaluación completada para {len(puntos)} puntos")
            
            # Desplazar para ver los nuevos resultados
            self.texto_resultados.see(tk.END)
        
        except Exception as e:
            # Manejar errores
            mensaje_error = str(e)
            self.var_estado.set(f"Error: {mensaje_error}")
            messagebox.showerror("Error", mensaje_error)
    
    def guardar_informe(self):
        """Guardar un informe completo en un archivo."""
        # Obtener parámetros de la función
        try:
            x0 = float(self.entrada_x0.get())
            ordenes = self.obtener_ordenes_seleccionados()
        except ValueError:
            messagebox.showerror("Error", "Parámetros inválidos")
            return
        
        # Obtener puntos de evaluación
        puntos_str = self.entrada_puntos_eval.get()
        try:
            puntos = [float(x.strip()) for x in puntos_str.split(",")]
        except ValueError:
            messagebox.showerror("Error", "Puntos de evaluación inválidos")
            return
        
        # Pedir directorio para guardar informe
        directorio_salida = filedialog.askdirectory(title="Seleccione directorio para guardar el informe")
        if not directorio_salida:
            return
        
        # Actualizar estado
        self.var_estado.set("Generando informe...")
        self.root.update_idletasks()
        
        # Ejecutar generación de informe en un hilo separado
        threading.Thread(target=self.generar_informe_completo, 
                         args=(x0, ordenes, puntos, directorio_salida)).start()
    
    def generar_informe_completo(self, x0, ordenes, puntos, directorio_salida):
        """Función de hilo para guardar informe."""
        try:
            # Generar el informe
            archivo_informe = self.taylor.generar_informe(x0, ordenes, puntos, directorio_salida)
            
            # Actualizar estado
            self.var_estado.set(f"Informe guardado en: {archivo_informe}")
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Informe Generado", 
                              f"El informe se ha guardado exitosamente en:\n{archivo_informe}")
        
        except Exception as e:
            # Manejar errores
            mensaje_error = str(e)
            self.var_estado.set(f"Error: {mensaje_error}")
            messagebox.showerror("Error", mensaje_error)

def main():
    """Función principal para ejecutar la aplicación de interfaz gráfica."""
    root = tk.Tk()
    app = InterfazTaylor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
