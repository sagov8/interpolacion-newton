# Interpolación Newton

Una aplicación interactiva para visualizar y aprender sobre el **método de interpolación de Newton**, con una interfaz gráfica que facilita la comprensión de este importante método numérico.

## 📋 Descripción

Este proyecto implementa el método de interpolación de Newton, un algoritmo fundamental en análisis numérico para aproximar funciones a partir de puntos de datos. La aplicación proporciona:

- **Visualización gráfica** de polinomios interpolantes
- **Cálculo automático** de diferencias divididas
- **Tablas interactivas** con resultados numéricos
- **Explicaciones detalladas** del proceso paso a paso
- **Presets predefinidos** para fácil experimentación

## 🚀 Características

- Interfaz intuitiva y responsiva
- Gráficos interactivos para visualizar interpolaciones
- Cálculo de diferencias divididas de Newton
- Tablas detalladas de resultados
- Explicaciones educativas del algoritmo
- Presets de ejemplo para aprendizaje rápido

## 📦 Estructura del Proyecto

```
interpolacion-newton/
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias del proyecto
├── core/
│   └── newton.py         # Implementación del método de Newton
├── data/
│   └── presets.py        # Conjuntos de datos predefinidos
└── ui/
    ├── charts.py         # Módulo de gráficos
    ├── explanations.py   # Explicaciones educativas
    ├── sidebar.py        # Barra lateral de la interfaz
    └── tables.py         # Tablas de datos
```

## 🔧 Requisitos

- Python 3.7+
- Las dependencias están listadas en `requirements.txt`

## 💻 Instalación

1. Clona el repositorio:
```bash
git clone <url-del-repositorio>
cd interpolacion-newton
```

2. Crea un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
venv\Scripts\activate  # En Windows
source venv/bin/activate  # En Linux/Mac
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## ▶️ Uso

Ejecuta la aplicación principal:

```bash
python app.py
```

La interfaz gráfica se abrirá y podrás:
- Seleccionar un preset o ingresar datos personalizados
- Ver la visualización gráfica de la interpolación
- Consultar las tablas con cálculos detallados
- Leer explicaciones sobre el proceso

## Método de Interpolación de Newton

El método de Newton utiliza diferencias divididas para construir un polinomio interpolante. Es especialmente útil porque:

- Permite agregar puntos nuevos sin recalcular todo desde cero
- Es numéricamente eficiente
- Proporciona una forma recursiva elegante

### Polinomio de Newton

$$P_n(x) = f[x_0] + f[x_0,x_1](x-x_0) + f[x_0,x_1,x_2](x-x_0)(x-x_1) + \ldots$$

Donde $f[x_i, x_{i+1}, \ldots]$ representa las diferencias divididas.

## 🎓 Aplicaciones Educativas

Este proyecto es útil para:
- Estudiantes de ingeniería y matemáticas
- Cursos de análisis numérico
- Problemas de aproximación de funciones
- Interpolación de datos experimentales

## Licencia

Este proyecto fue creado con fines educativos.

## Autor

Santiago Vivas

## 📧 Contacto

Para preguntas o sugerencias, por favor abre un _issue_ en el repositorio.

---

**Nota**: Esta es una herramienta educativa. Para aplicaciones críticas, se recomienda validar los resultados con software numérico especializado.
