# RandomWalk Simulator

Simulador de caminata aleatoria (Random Walk) en 1D, 2D y 3D con visualización, animación y análisis estadístico.

## Estructura del proyecto

- `main_gui.py`: aplicación principal con interfaz (CustomTkinter).
- `config.py`: constantes del generador congruencial lineal (A, C, M y semilla por defecto).
- `generators/gcl.py`: generador de números pseudo-aleatorios (GCL).
- `models/walk_1d.py`, `walk_2d.py`, `walk_3d.py`: funciones de trayectoria y caminata.
- `simulations/multiple_runs.py`, `multiple_runs_2d.py`, `multiple_runs_3d.py`: simulaciones de múltiples corridas.
- `visualization/`: gráficos de trayectoria, animaciones, histogramas y análisis.
- `services/test_runner.py`: tests de calidad de aleatoriedad (chi-cuadrado, KS, media, varianza, runs, poker, etc.)
- `resultados_1d.csv`, `resultados_2d.csv`, `resultados_3d.csv`: ejemplos de salida generada por la aplicación.

## Requisitos

- Python 3.10+ (probado con Python 3.14) 
- Paquetes: `matplotlib`, `customtkinter`.

Instalar dependencias:

```bash
python -m pip install matplotlib customtkinter
```

## Ejecución

Ejecuta la interfaz:

```bash
python main_gui.py
```

### Uso desde GUI

1. Selecciona dimensión: `1D`, `2D`, `3D`.
2. Ingresa número de `saltos` (p.ej. 1000).
3. Ingresa `semilla` (p.ej. 12345).
4. Ingresa `simulaciones` (p.ej. 100). Este valor se usa solo en `Múltiples`.
5. Botones:
   - `Ejecutar`: calcula trayectoria y grafica (también corre tests de aleatoriedad y muestra resultados).
   - `Animar`: muestra animación de la trayectoria en dimensiones 1D/2D/3D.
   - `Múltiples`: corre `simulaciones` corridas, genera análisis y guarda CSV (resultados_1d.csv / resultados_2d.csv / resultados_3d.csv).

## Resultados y archivos generados

- `histograma_1d`: histograma de posiciones finales para 1D (múltiples corridas).
- `scatter_2d`, `scatter_3d`: nubes de puntos de posiciones finales para 2D/3D.
- `plot_analisis`: visualiza datos de análisis según dimensión.
- CSV: guarda resultados de posiciones finales en la raíz con nombre según dimensión.

## Pruebas de aleatoriedad

`services/test_runner.py` ejecuta (al presionar `Ejecutar`):
- Chi-cuadrado
- KS
- medias
- varianzas
- poker
- corridas (runs test)

## Configuración del generador

En `config.py`:
- `A = 1664525`
- `C = 1013904223`
- `M = 2**32`
- `DEFAULT_SEED = 12345`

Estos parámetros se usan en `generators/gcl.py` (congruencial lineal).

## Notas

- El generador se reinicia apropiadamente entre ejecuciones y simulaciones.
- Para cambios experimentales, modifica `models/*` o `visualization/*`.
- En 3D, se requiere `matplotlib` con soporte 3D (viene con librerías normales de matplotlib).

---
