import matplotlib.pyplot as plt
import numpy as np

def histograma_1d(resultados):

    media = np.mean(resultados)
    desviacion = np.std(resultados)

    plt.figure()

    # Histograma
    plt.hist(resultados, bins=30, density=True, alpha=0.6, label="Simulaciones")

    # Curva normal teórica
    x = np.linspace(min(resultados), max(resultados), 1000)
    y = (1 / (desviacion * np.sqrt(2 * np.pi))) * np.exp(
        -0.5 * ((x - media) / desviacion) ** 2
    )

    plt.plot(x, y, 'r-', label="Normal teórica")

    plt.title("Distribución de posiciones finales (Caminata 1D)")
    plt.xlabel("Posición final")
    plt.ylabel("Densidad")

    # Líneas de referencia
    plt.axvline(media, linestyle="--", label=f"Media = {media:.2f}")

    plt.legend()
    plt.grid()

    plt.show()