import customtkinter as ctk
from tkinter import messagebox
import time

from generators.gcl import GCL
from config import A, C, M

from models.walk_1d import trayectoria_1d, caminata_1d
from models.walk_2d import trayectoria_2d
from models.walk_3d import trayectoria_3d

from visualization.plot_1d import plot_1d
from visualization.plot_2d import plot_2d
from visualization.plot_3d import plot_3d

from visualization.anim_1d import animar_1d
from visualization.anim_2d import animar_2d
from visualization.anim_3d import animar_3d

from visualization.analysis_plot import plot_analisis

from visualization.hist_1d import histograma_1d

from services.test_runner import TestRunner

import matplotlib.pyplot as plt

import csv

#  Configuración global de la apariencia de la interfaz
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    """Clase principal de la aplicación GUI para el simulador.

    Contiene la ventana, los widgets de control y las funciones
    que invocan los cálculos y las visualizaciones.
    """

    def __init__(self):
        super().__init__()

        # Configuración inicial de la ventana
        self.title("🐸 Random Walk Simulator")
        self.geometry("500x600")

        # Crear controles de la interfaz
        self.create_widgets()

    def create_widgets(self):
        """Crea y organiza los widgets de entrada y botones."""

        # Título principal
        title = ctk.CTkLabel(self, text="Simulador de Caminata Aleatoria", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        # Contenedor principal para inputs y botones
        frame = ctk.CTkFrame(self)
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Selección de dimensión (1D/2D/3D)
        ctk.CTkLabel(frame, text="Dimensión").pack(pady=5)
        self.dimension = ctk.CTkOptionMenu(frame, values=["1D", "2D", "3D"])
        self.dimension.pack(pady=5)

        # Entrada para número de saltos de la caminata
        ctk.CTkLabel(frame, text="Número de saltos").pack(pady=5)
        self.saltos = ctk.CTkEntry(frame)
        self.saltos.insert(0, "1000")
        self.saltos.pack(pady=5)

        # Entrada para semilla del generador de números aleatorios
        ctk.CTkLabel(frame, text="Semilla").pack(pady=5)
        self.semilla = ctk.CTkEntry(frame)
        self.semilla.insert(0, "12345")
        self.semilla.pack(pady=5)

        # Entrada para cantidad de simulaciones múltiples
        ctk.CTkLabel(frame, text="Simulaciones").pack(pady=5)
        self.simulaciones = ctk.CTkEntry(frame)
        self.simulaciones.insert(0, "100")
        self.simulaciones.pack(pady=5)

        # Botones de acción
        ctk.CTkButton(frame, text="▶ Ejecutar", command=self.ejecutar).pack(pady=10)
        ctk.CTkButton(frame, text="🎬 Animar", command=self.animar).pack(pady=10)
        ctk.CTkButton(frame, text="📊 Múltiples", command=self.multiple).pack(pady=10)

    def guardar_csv(self, nombre_archivo, datos, dimension):
        """Guarda los resultados de simulación en un archivo CSV.

        :param nombre_archivo: nombre de archivo destino
        :param datos: lista de tuplas de resultados por simulación
        :param dimension: cadena "1D", "2D", o "3D" para encabezados
        """
        with open(nombre_archivo, mode="w", newline="") as file:
            writer = csv.writer(file)

            # Encabezados según dimensión
            if dimension == "1D":
                writer.writerow(["Simulacion", "Posicion Final"])
            elif dimension == "2D":
                writer.writerow(["Simulacion", "X Final", "Y Final"])
            elif dimension == "3D":
                writer.writerow(["Simulacion", "X Final", "Y Final", "Z Final"])

            # Escribir datos
            for i, fila in enumerate(datos):
                writer.writerow([i + 1] + list(fila))

        print(f"CSV guardado como: {nombre_archivo}")

    def generar_randoms_globales(sims, saltos, seed):
        """Genera una lista de números pseudoaleatorios para todas las simulaciones.

        :param sims: número de simulaciones
        :param saltos: número de saltos por simulación
        :param seed: semilla inicial
        :return: lista de valores aleatorios generados para todas las simulaciones
        """
        todos = []

        for i in range(sims):
            rng = GCL(seed + i, A, C, M)
            todos.extend(rng.generate_sequence(saltos))

        return todos

    def get_inputs(self):
        """Lee y valida los valores de los campos de entrada."""
        try:
            return (
                self.dimension.get(),
                int(self.saltos.get()),
                int(self.semilla.get()),
                int(self.simulaciones.get())
            )
        except:
            messagebox.showerror("Error", "Valores inválidos")
            return None

    def ejecutar(self):
        """Ejecuta una simulación individual y muestra los resultados.

        - Valida la entrada.
        - Crea el generador GCL con la semilla indicada.
        - Genera los números aleatorios y reinicia el RNG antes de simular.
        - Traza la trayectoria según la dimensión seleccionada.
        - Ejecuta tests de aleatoriedad sobre los valores generados.
        - Muestra métricas de tiempo por paso.
        """
        datos = self.get_inputs()
        if not datos:
            return

        inicio_total = time.perf_counter()

        dim, saltos, semilla, _ = datos
        rng = GCL(semilla, A, C, M)

        # Mide el tiempo de generación de valores pseudoaleatorios
        t0 = time.perf_counter()
        randoms = rng.generate_sequence(saltos)
        t1 = time.perf_counter()

        # Reiniciar la semilla para la simulación de la trayectoria
        rng.reset()

        # Mide el tiempo de simulación y graficado
        t2 = time.perf_counter()

        if dim == "1D":
            plot_1d(trayectoria_1d(saltos, rng))
        elif dim == "2D":
            x, y = trayectoria_2d(saltos, rng)
            plot_2d(x, y)
        elif dim == "3D":
            x, y, z = trayectoria_3d(saltos, rng)
            plot_3d(x, y, z)

        t3 = time.perf_counter()

        # Ejecuta el conjunto de tests de aleatoriedad
        t4 = time.perf_counter()
        tester = TestRunner()
        resultados = tester.run_all_tests(randoms)
        t5 = time.perf_counter()

        fin_total = time.perf_counter()

        # Ventana con resultados de tests
        self.mostrar_resultados_tests(resultados)

        # Imprimir los tiempos de cada etapa en consola
        print("\nTIEMPOS DE EJECUCIÓN:")
        print(f"Generación randoms: {t1 - t0:.4f} s")
        print(f"Simulación: {t3 - t2:.4f} s")
        print(f"Tests: {t5 - t4:.4f} s")
        print(f"TOTAL: {fin_total - inicio_total:.4f} s")

    def animar(self):
        """Muestra la animación de la caminata en la dimensión seleccionada."""
        datos = self.get_inputs()
        if not datos:
            return

        dim, saltos, semilla, _ = datos
        rng = GCL(semilla, A, C, M)

        if dim == "1D":
            animar_1d(saltos, rng)
        elif dim == "2D":
            animar_2d(saltos, rng)
        elif dim == "3D":
            animar_3d(saltos, rng)

    def prob_retorno(self, simulaciones, dim):
        """Calcula la proporción de simulaciones que retornan al origen.

        :param simulaciones: lista de posiciones finales (1D, 2D o 3D)
        :param dim: dimensión como cadena "1D"/"2D"/"3D"
        :return: fracción de simulaciones donde la posición final es el origen
        """
        count = 0

        for pos in simulaciones:
            if dim == "1D" and pos == 0:
                count += 1
            elif dim == "2D" and pos == (0, 0):
                count += 1
            elif dim == "3D" and pos == (0, 0, 0):
                count += 1

        return count / len(simulaciones) if simulaciones else 0

    def multiple(self):
        """Ejecuta múltiples simulaciones y muestra estadísticas + tests."""
        datos = self.get_inputs()
        if not datos:
            return

        inicio_total = time.perf_counter()  

        dim, saltos, semilla, sims = datos

        todos_los_randoms = []

        # ⏱RANDOMS
        t0 = time.perf_counter()

        if dim == "1D":
            resultados = []
            finales = []

            # Generar simulaciones 1D y datos de randoms
            for i in range(sims):
                rng = GCL(semilla + i, A, C, M)

                randoms = rng.generate_sequence(saltos)
                todos_los_randoms.extend(randoms)

                resultado = caminata_1d(saltos, GCL(semilla + i, A, C, M))
                resultados.append(resultado)
                finales.append((resultado,))

            # Probabilidad de regreso al origen (1D para la lista de posiciones finales)
            prob = self.prob_retorno([f[0] for f in finales], "1D")
            print(f"Probabilidad de retorno al origen: {prob:.4f}")

            t1 = time.perf_counter()

            #  VISUALIZACIÓN
            t2 = time.perf_counter()

            histograma_1d(resultados)
            plot_analisis(finales, "1D")

            t3 = time.perf_counter()

            self.guardar_csv("resultados_1d.csv", finales, "1D")

        elif dim == "2D":
            from simulations.multiple_runs_2d import multiples_simulaciones_2d
            from visualization.scatter_2d import scatter_2d

            for i in range(sims):
                rng = GCL(semilla + i, A, C, M)
                todos_los_randoms.extend(rng.generate_sequence(saltos))

            t1 = time.perf_counter()

            t2 = time.perf_counter()

            x, y = multiples_simulaciones_2d(sims, saltos, semilla)
            scatter_2d(x, y)

            finales = list(zip(x, y))
            prob = self.prob_retorno(finales, "2D")
            print(f"Probabilidad de retorno al origen: {prob:.4f}")
            plot_analisis(finales, "2D")

            t3 = time.perf_counter()

            self.guardar_csv("resultados_2d.csv", finales, "2D")

        elif dim == "3D":
            from simulations.multiple_runs_3d import multiples_simulaciones_3d
            from visualization.scatter_3d import scatter_3d

            for i in range(sims):
                rng = GCL(semilla + i, A, C, M)
                todos_los_randoms.extend(rng.generate_sequence(saltos))

            t1 = time.perf_counter()

            t2 = time.perf_counter()

            x, y, z = multiples_simulaciones_3d(sims, saltos, semilla)
            scatter_3d(x, y, z)

            finales = list(zip(x, y, z))
            prob = self.prob_retorno(finales, "3D")
            print(f"Probabilidad de retorno al origen: {prob:.4f}")
            plot_analisis(finales, "3D")

            t3 = time.perf_counter()

            self.guardar_csv("resultados_3d.csv", finales, "3D")

        #  TESTS
        t4 = time.perf_counter()

        tester = TestRunner()
        test_results = tester.run_all_tests(todos_los_randoms)

        t5 = time.perf_counter()

        self.mostrar_resultados_tests(test_results)

        fin_total = time.perf_counter()

        # RESULTADOS DE TIEMPO
        print("\nTIEMPOS DE EJECUCIÓN (MÚLTIPLE):")
        print(f"Randoms + simulación: {t1 - t0:.4f} s")
        print(f"Visualización: {t3 - t2:.4f} s")
        print(f"Tests: {t5 - t4:.4f} s")
        print(f"TOTAL: {fin_total - inicio_total:.4f} s")

    def mostrar_resultados_tests(self, resultados):
        """Muestra los resultados de los tests en una ventana modal."""
        # Crear ventana nueva
        ventana = ctk.CTkToplevel(self)
        ventana.title("Resultados de Tests")
        ventana.geometry("400x400")

        titulo = ctk.CTkLabel(
            ventana, 
            text="RESULTADOS DE PRUEBAS", 
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=15)

        frame = ctk.CTkFrame(ventana)
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        nombres = {
            "chi_square": "Chi-Cuadrado",
            "ks_test": "Kolmogorov-Smirnov",
            "mean_test": "Media",
            "variance_test": "Varianza",
            "poker_test": "Poker",
            "runs_test": "Runs"
        }

        # Mostrar cada test
        for key, nombre in nombres.items():
            test = resultados.get(key, {})

            if not test:
                estado = "⚠️ No ejecutado"
                color = "gray"
            elif "error" in test:
                estado = "❌ Error"
                color = "orange"
            elif test.get("passed", False):
                estado = "✅ APROBADO"
                color = "green"
            else:
                estado = "❌ RECHAZADO"
                color = "red"

            fila = ctk.CTkFrame(frame)
            fila.pack(fill="x", pady=5, padx=10)

            label_nombre = ctk.CTkLabel(fila, text=nombre)
            label_nombre.pack(side="left", padx=10)

            label_estado = ctk.CTkLabel(fila, text=estado, text_color=color)
            label_estado.pack(side="right", padx=10)

       
if __name__ == "__main__":
    app = App()
    app.mainloop()