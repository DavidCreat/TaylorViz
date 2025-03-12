# TaylorViz: Herramienta Avanzada de Aproximación de Series de Taylor

## Visualización y Análisis de Aproximaciones de Series de Taylor

## 📋 Descripción

TaylorViz es una herramienta matemática avanzada que permite calcular, visualizar y analizar aproximaciones de series de Taylor para funciones matemáticas arbitrarias. Diseñada tanto para estudiantes como para profesionales, esta herramienta combina precisión matemática con visualizaciones interactivas para facilitar la comprensión de conceptos fundamentales del cálculo.

## ✨ Características

| 🧮 **Cálculo Preciso** | Aproximaciones de Taylor hasta orden 200 con alta precisión numérica |
|------------------------|---------------------------------------------------------------------|
| 📈 **Visualización Interactiva** | Gráficos dinámicos para comparar funciones originales con sus aproximaciones |
| 📉 **Análisis de Error** | Cálculo y visualización de errores de truncamiento y límites teóricos |
| 🔄 **Múltiples Interfaces** | GUI intuitiva, CLI potente y API programática para integración |
| ⚡ **Procesamiento Optimizado** | Soporte para cálculo paralelo en sistemas multicore |
| 📊 **Exportación de Resultados** | Generación de informes detallados y exportación de gráficos |

## 🚀 Instalación

### Requisitos Previos

* Python 3.6 o superior
* Pip (gestor de paquetes de Python)

### Instalación de Dependencias

```bash
# Clonar el repositorio
git clone https://github.com/DavidCreat/TaylorViz.git
cd TaylorViz

# Instalar dependencias
pip install -r requirements.txt
```

## 🖥️ Interfaces

TaylorViz ofrece tres interfaces diferentes para adaptarse a distintas necesidades:

| Interfaz Gráfica (GUI) | Línea de Comandos (CLI) | API Programática |
|------------------------|-------------------------|------------------|
| ![GUI Demo](https://i.ibb.co/FkKpnj8X/image.png) | ![CLI Demo](https://i.ibb.co/sMn7bHN/image.png) |
| **Ejecución:** `python gui.py`<br>**Ideal para:** Exploración interactiva y visualización en tiempo real | **Ejecución:** `python main.py -f "sin(x)" -x0 0 -o 5`<br>**Ideal para:** Automatización, scripts y entornos sin GUI | **Importación:** `from taylor_series import AproximacionTaylor`<br>**Ideal para:** Integración en otros proyectos Python |

### 1. Interfaz Gráfica (GUI)

La interfaz gráfica proporciona una experiencia interactiva completa con visualizaciones en tiempo real.

**Características de la GUI:**
* Entrada intuitiva de funciones matemáticas
* Visualización en tiempo real de aproximaciones
* Pestañas separadas para aproximaciones y análisis de error
* Evaluación interactiva en puntos específicos
* Exportación de resultados y gráficos

### 2. Interfaz de Línea de Comandos (CLI)

Ideal para automatización, scripts y uso en entornos sin interfaz gráfica.

**Parámetros Principales:**
* `-f, --funcion`: Función a aproximar (sintaxis de SymPy)
* `-x0, --punto-expansion`: Punto alrededor del cual expandir
* `-o, --orden`: Orden máximo de la aproximación
* `-p, --graficar`: Generar visualizaciones
* `-e, --evaluar`: Puntos específicos para evaluar
* `--paralelo`: Activar procesamiento en paralelo

### 3. API Programática

Importa la clase `AproximacionTaylor` directamente en tus proyectos Python:

```python
from taylor_series import AproximacionTaylor

# Crear instancia
taylor = AproximacionTaylor()

# Configurar función
taylor.establecer_funcion("sin(x)")

# Calcular aproximación
aproximacion = taylor.visualizar_serie_taylor(x0=0, orden=5)

# Visualizar resultados
taylor.graficar_aproximaciones(x0=0, ordenes=[1, 3, 5], rango_x=(-2, 2))
```

## 📊 Ejemplos

### Ejemplo 1: Aproximación Básica
```bash
python main.py -f "sin(x)" -x0 0 -o 5
```
Calcula una aproximación de orden 5 para la función seno alrededor de x=0.

<details>
<summary>Ver resultado</summary>

La aproximación resultante es: x - x³/6 + x⁵/120

![Aproximación sin(x)](https://i.ibb.co/wrMf6BYP/image.png)
</details>

### Ejemplo 2: Comparación de Órdenes
```bash
python main.py -f "cos(x)" -x0 0 -o 8 -p -c 2 4 6 -r -3.14 3.14
```
Compara aproximaciones de diferentes órdenes para el coseno en un rango de -π a π.

### Ejemplo 3: Análisis de Error
```bash
python main.py -f "exp(x)" -x0 0 -o 6 -p -e 0.5 1.0 1.5 -s "resultados_exp"
```
Analiza el error de truncamiento para la función exponencial en varios puntos.

### Ejemplo 4: Funciones Complejas
```bash
python main.py -f "sin(x)/x if x != 0 else 1" -x0 0 -o 10 -p --paralelo
```
Aproxima una función con discontinuidad removible usando procesamiento paralelo.

### Funciones Matemáticas Soportadas

TaylorViz utiliza la sintaxis de SymPy para las expresiones matemáticas, soportando una amplia variedad de funciones:

| Categoría | Ejemplos | Descripción |
|-----------|----------|-------------|
| **Trigonométricas** | `sin(x), cos(x), tan(x), atan(x)` | Funciones trigonométricas estándar |
| **Exponenciales** | `exp(x), log(x), log10(x)` | Funciones exponenciales y logarítmicas |
| **Algebraicas** | `x**n, sqrt(x), abs(x)` | Operaciones algebraicas básicas |
| **Hiperbólicas** | `sinh(x), cosh(x), tanh(x)` | Funciones hiperbólicas |
| **Especiales** | `erf(x), gamma(x), besselj(n,x)` | Funciones especiales matemáticas |
| **Combinadas** | `sin(x)*exp(-x**2), log(1+x)/x` | Combinaciones arbitrarias de funciones |

## 📖 Documentación

### Fundamentos Teóricos

La serie de Taylor es una representación de una función como una suma infinita de términos calculados a partir de los valores de las derivadas de la función en un punto específico.

Para una función f(x) alrededor del punto x₀, la serie de Taylor se define como:

```
f(x) ≈ f(x₀) + f'(x₀)(x-x₀) + f''(x₀)(x-x₀)²/2! + f'''(x₀)(x-x₀)³/3! + ...
```

```
f(x) ≈ ∑(n=0 a ∞) f^(n)(x₀)(x-x₀)^n/n!
```

El error de truncamiento al usar los primeros N términos está acotado por:

```
|E_N(x)| ≤ M_(N+1)|x-x₀|^(N+1)/(N+1)!
```

donde M_(N+1) es el máximo valor de |f^(N+1)(ξ)| en el intervalo entre x₀ y x.

### API de Referencia

| Método | Descripción | Parámetros | Retorno |
|--------|-------------|------------|---------|
| `establecer_funcion(func_str)` | Define la función a aproximar | `func_str`: String con la expresión de la función | None |
| `derivar_funcion(x0, orden)` | Calcula la derivada n-ésima en x0 | `x0`: Punto de evaluación<br>`orden`: Orden de la derivada | Valor numérico de la derivada |
| `analizar_termino_taylor(x0, n)` | Calcula el n-ésimo término de la serie | `x0`: Punto de expansión<br>`n`: Orden del término | Expresión simbólica del término |
| `visualizar_serie_taylor(x0, orden)` | Calcula la aproximación completa | `x0`: Punto de expansión<br>`orden`: Orden máximo | Expresión simbólica de la serie |
| `integrar_error_taylor(x0, orden, punto)` | Calcula el error en un punto específico | `x0`: Punto de expansión<br>`orden`: Orden de aproximación<br>`punto`: Punto de evaluación | Valor numérico del error |
| `determinar_limite_error(x0, orden, punto)` | Calcula una cota superior del error | `x0`: Punto de expansión<br>`orden`: Orden de aproximación<br>`punto`: Punto de evaluación | Valor numérico de la cota |
| `graficar_aproximaciones(...)` | Genera gráficos de aproximaciones | `x0`: Punto de expansión<br>`ordenes`: Lista de órdenes<br>`rango_x`: Rango de visualización | Objeto de figura |
| `generar_informe(...)` | Crea un informe completo | `x0`: Punto de expansión<br>`ordenes`: Lista de órdenes<br>`puntos`: Puntos a evaluar<br>`directorio`: Ruta de salida | Ruta del archivo generado |

### Opciones de Línea de Comandos

```
uso: main.py [-h] -f FUNCION -x0 PUNTO_EXPANSION -o ORDEN [-e EVALUAR [EVALUAR ...]] 
           [-p] [-r MIN MAX] [-c COMPARAR [COMPARAR ...]] [-s GUARDAR] [--paralelo]

Calcula aproximaciones de series de Taylor y errores de truncamiento.

opciones:
  -h, --help            muestra este mensaje de ayuda y sale
  -f FUNCION, --funcion FUNCION
                        Función a aproximar (en términos de x, usando sintaxis de SymPy)
  -x0 PUNTO_EXPANSION, --punto-expansion PUNTO_EXPANSION
                        Punto alrededor del cual expandir la serie de Taylor
  -o ORDEN, --orden ORDEN
                        Orden de la aproximación de Taylor (máximo 200)
  -e EVALUAR [EVALUAR ...], --evaluar EVALUAR [EVALUAR ...]
                        Puntos en los que evaluar la aproximación
  -p, --graficar        Generar gráficas de la aproximación y errores
  -r MIN MAX, --rango MIN MAX
                        Rango para graficar (min_x max_x)
  -c COMPARAR [COMPARAR ...], --comparar COMPARAR [COMPARAR ...]
                        Comparar múltiples órdenes de aproximación
  -s GUARDAR, --guardar GUARDAR
                        Guardar resultados en el directorio especificado
  --paralelo            Usar cálculo en paralelo para mejor rendimiento
```

### Guía de la Interfaz Gráfica

La interfaz gráfica de TaylorViz está diseñada para ser intuitiva y fácil de usar:

1. **Panel de Entrada**: Introduce la función, punto de expansión y orden
2. **Funciones Predefinidas**: Selecciona funciones comunes de la lista desplegable
3. **Visualización**: Observa la aproximación y la función original en la gráfica principal
4. **Análisis de Error**: Cambia a la pestaña de error para ver la precisión de la aproximación
5. **Evaluación de Puntos**: Introduce puntos específicos para calcular valores exactos y aproximados
6. **Exportación**: Guarda gráficos e informes completos con el botón "Guardar Informe"

### Consejos Avanzados

* **Rendimiento**: Para funciones complejas o aproximaciones de orden alto, use la opción `--paralelo` en CLI o active el procesamiento paralelo en la GUI
* **Precisión Numérica**: Para mejorar la precisión en puntos lejanos al punto de expansión, considere usar órdenes más altos o múltiples expansiones en diferentes puntos
* **Visualización Óptima**: Ajuste el rango de visualización para centrarse en regiones de interés, especialmente cuando la función tiene comportamientos diferentes en distintas regiones
* **Funciones con Singularidades**: Tenga cuidado al aproximar funciones cerca de sus singularidades; las series de Taylor pueden no converger adecuadamente
* **Exportación**: Use la opción `-s` para guardar todos los resultados y gráficos para análisis posterior

## 🔧 Solución de Problemas

<details>
<summary><strong>Error al instalar dependencias</strong></summary>

Si encuentras problemas al instalar las dependencias, intenta:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Para sistemas Linux, es posible que necesites instalar bibliotecas adicionales:

```bash
sudo apt-get install python3-dev libffi-dev
```
</details>

<details>
<summary><strong>Problemas con la interfaz gráfica</strong></summary>

Si la interfaz gráfica no se inicia correctamente:

1. Verifica que tienes instalado Tkinter:
   ```bash
   python -c "import tkinter; tkinter._test()"
   ```

2. En Linux, puedes necesitar instalar el paquete:
   ```bash
   sudo apt-get install python3-tk
   ```
</details>

<details>
<summary><strong>Errores en cálculos con funciones complejas</strong></summary>

Para funciones complejas o con singularidades:

1. Intenta usar un orden mayor para la aproximación
2. Asegúrate de que el punto de expansión no esté cerca de una singularidad
3. Considera usar la opción de procesamiento paralelo para cálculos más precisos
</details>

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor, siga estos pasos para contribuir:

1. Fork el repositorio
2. Cree una rama para su característica (`git checkout -b feature/amazing-feature`)
3. Commit sus cambios (`git commit -m 'Add some amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abra un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - vea el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor
 
 <div align="center">
   <a href="https://github.com/DavidCreat">
     <img src="https://github.com/DavidCreat.png" width="100px" alt="David Fonseca" style="border-radius:50%;">
   </a>
   
   <h3>David Fonseca</h3>
   <p>Desarrollador Full Stack | Entusiasta de DevOps | Creador de Experiencias Web Innovadoras</p>
   
   <p>
     <a href="https://eas1.com.es/" target="_blank">
       <img src="https://img.shields.io/badge/Website-eas1.com.es-blue?style=flat-square&logo=google-chrome&logoColor=white" alt="Website">
     </a>
     <a href="https://github.com/DavidCreat" target="_blank">
       <img src="https://img.shields.io/badge/GitHub-DavidCreat-181717?style=flat-square&logo=github" alt="GitHub">
     </a>
     <a href="https://orcid.org/0009-0001-5972-2687" target="_blank">
       <img src="https://img.shields.io/badge/ORCID-0009--0001--5972--2687-green?style=flat-square&logo=orcid&logoColor=white" alt="ORCID">
     </a>
   </p>
 </div>
 
 ---
 
 <div align="center">
   <p>Desarrollado con ❤️ por <a href="https://github.com/DavidCreat">David Fonseca</a></p>
   <p>© 2025 - Todos los derechos reservados</p>
 </div>
