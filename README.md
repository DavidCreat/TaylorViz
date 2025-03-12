# TaylorViz: Herramienta Avanzada de Aproximación de Series de Taylor

<div align="center">
  <p>
    <strong>Visualización y Análisis de Aproximaciones de Series de Taylor</strong>
  </p>
  
  <p>
    <a href="#características">Características</a> •
    <a href="#instalación">Instalación</a> •
    <a href="#interfaces">Interfaces</a> •
    <a href="#ejemplos">Ejemplos</a> •
    <a href="#documentación">Documentación</a> •
    <a href="#licencia">Licencia</a>
  </p>
</div>

## 📋 Descripción

TaylorViz es una herramienta matemática avanzada que permite calcular, visualizar y analizar aproximaciones de series de Taylor para funciones matemáticas arbitrarias. Diseñada tanto para estudiantes como para profesionales, esta herramienta combina precisión matemática con visualizaciones interactivas para facilitar la comprensión de conceptos fundamentales del cálculo.

## ✨ Características

- **Cálculo Preciso**: Aproximaciones de Taylor hasta orden 200 con alta precisión numérica
- **Visualización Interactiva**: Gráficos dinámicos para comparar funciones originales con sus aproximaciones
- **Análisis de Error**: Cálculo y visualización de errores de truncamiento y límites teóricos
- **Múltiples Interfaces**:
  - Interfaz gráfica intuitiva (GUI)
  - Interfaz de línea de comandos (CLI)
  - API programática para integración en otros proyectos
- **Procesamiento Optimizado**: Soporte para cálculo paralelo en sistemas multicore
- **Exportación de Resultados**: Generación de informes detallados y exportación de gráficos

## 🚀 Instalación

### Requisitos Previos

- Python 3.6 o superior
- Pip (gestor de paquetes de Python)

### Instalación de Dependencias

```bash
# Instalar dependencias
pip install -r requirements.txt
```

## 🖥️ Interfaces

TaylorViz ofrece tres interfaces diferentes para adaptarse a distintas necesidades:

### 1. Interfaz Gráfica (GUI)

La interfaz gráfica proporciona una experiencia interactiva completa con visualizaciones en tiempo real.

**Ejecución:**
```bash
python gui.py
```

**Características de la GUI:**
- Entrada intuitiva de funciones matemáticas
- Visualización en tiempo real de aproximaciones
- Pestañas separadas para aproximaciones y análisis de error
- Evaluación interactiva en puntos específicos
- Exportación de resultados y gráficos

### 2. Interfaz de Línea de Comandos (CLI)

Ideal para automatización, scripts y uso en entornos sin interfaz gráfica.

**Uso Básico:**
```bash
python main.py -f "sin(x)" -x0 0 -o 5
```

**Parámetros Principales:**
- `-f, --funcion`: Función a aproximar (sintaxis de SymPy)
- `-x0, --punto-expansion`: Punto alrededor del cual expandir
- `-o, --orden`: Orden máximo de la aproximación
- `-p, --graficar`: Generar visualizaciones
- `-e, --evaluar`: Puntos específicos para evaluar
- `--paralelo`: Activar procesamiento en paralelo

### 3. API Programática

Importa la clase `AproximacionTaylor` directamente en tus proyectos Python:

```python
from taylor_series import AproximacionTaylor

# Crear instancia
taylor = AproximacionTaylor()

# Configurar función
taylor.establecer_funcion("sin(x)")

# Calcular aproximación
aproximacion = taylor.calcular_serie_taylor(x0=0, orden=5)

# Visualizar resultados
taylor.graficar_aproximaciones(x0=0, ordenes=[1, 3, 5], rango_x=(-2, 2))
```

## 📊 Ejemplos

### Ejemplo 1: Aproximación Básica

```bash
# Aproximación de orden 5 para sin(x) alrededor de x=0
python main.py -f "sin(x)" -x0 0 -o 5
```

### Ejemplo 2: Comparación de Órdenes

```bash
# Comparar aproximaciones de diferentes órdenes para cos(x)
python main.py -f "cos(x)" -x0 0 -o 8 -p -c 2 4 6 -r -3.14 3.14
```

### Ejemplo 3: Análisis de Error

```bash
# Analizar error de truncamiento para exp(x)
python main.py -f "exp(x)" -x0 0 -o 6 -p -e 0.5 1.0 1.5 -s "resultados_exp"
```

### Ejemplo 4: Funciones Complejas con Procesamiento Paralelo

```bash
# Aproximación de función compleja usando procesamiento paralelo
python main.py -f "sin(x)/x if x != 0 else 1" -x0 0 -o 10 -p --paralelo
```

## 📝 Funciones Matemáticas Soportadas

TaylorViz utiliza la sintaxis de SymPy para las expresiones matemáticas, soportando una amplia variedad de funciones:

| Categoría | Ejemplos |
|-----------|----------|
| **Trigonométricas** | `sin(x)`, `cos(x)`, `tan(x)`, `atan(x)` |
| **Exponenciales** | `exp(x)`, `log(x)`, `log10(x)` |
| **Algebraicas** | `x**n`, `sqrt(x)`, `abs(x)` |
| **Hiperbólicas** | `sinh(x)`, `cosh(x)`, `tanh(x)` |
| **Especiales** | `erf(x)`, `gamma(x)`, `besselj(n,x)` |
| **Combinadas** | `sin(x)*exp(-x**2)`, `log(1+x)/x` |

## 🔍 Visualizaciones Avanzadas

TaylorViz ofrece múltiples formas de visualizar y analizar las aproximaciones:

### 1. Gráficos de Aproximación

Compara visualmente la función original con sus aproximaciones de diferentes órdenes.

```bash
python main.py -f "log(1+x)" -x0 0 -o 6 -p -c 2 4 -r -0.9 2
```

### 2. Análisis de Error

Visualiza el error de truncamiento en escala logarítmica para diferentes órdenes.

```bash
python main.py -f "sin(x)" -x0 0 -o 8 -p -c 2 4 6 -r -3.14 3.14 -s "error_sin"
```

### 3. Visualización 3D (GUI)

La interfaz gráfica permite visualizar aproximaciones de funciones de dos variables en 3D.

### 4. Animaciones (GUI)

Explora cómo cambia la aproximación al modificar el orden o el punto de expansión mediante animaciones interactivas.

## 📖 Documentación

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

### Métodos Principales de la API

| Método | Descripción |
|--------|-------------|
| `establecer_funcion(func_str)` | Define la función a aproximar |
| `calcular_serie_taylor(x0, orden)` | Calcula la aproximación de Taylor |
| `calcular_error_truncamiento(x0, orden, x_val)` | Calcula el error en un punto específico |
| `graficar_aproximaciones(x0, ordenes, rango_x)` | Genera gráficos de aproximaciones |
| `graficar_errores(x0, ordenes, rango_x)` | Genera gráficos de errores |
| `generar_informe(x0, ordenes, x_eval, directorio)` | Crea un informe completo |

## 🔧 Consejos Avanzados

- **Rendimiento**: Para funciones complejas o aproximaciones de orden alto, use la opción `--paralelo`
- **Precisión Numérica**: Para mejorar la precisión en puntos lejanos al punto de expansión, considere usar órdenes más altos
- **Visualización Óptima**: Ajuste el rango de visualización con `-r` para centrarse en regiones de interés
- **Exportación**: Use la opción `-s` para guardar todos los resultados y gráficos para análisis posterior

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - vea el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor, abra un issue para discutir cambios importantes antes de enviar un pull request.

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
