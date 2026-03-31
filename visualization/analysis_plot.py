import matplotlib.pyplot as plt
import numpy as np

def plot_analisis(finales, dimension):
    """
    Muestra histograma + media + distancia al origen
    """

    if dimension == "1D":
        valores = np.array([f[0] for f in finales])
        distancias = np.abs(valores)

    elif dimension == "2D":
        valores = np.array([np.sqrt(x**2 + y**2) for x, y in finales])
        distancias = valores

    elif dimension == "3D":
        valores = np.array([np.sqrt(x**2 + y**2 + z**2) for x, y, z in finales])
        distancias = valores

    media = np.mean(valores)
    media_distancia = np.mean(distancias)

    # Histograma
    plt.figure()
    plt.hist(valores, bins=20)

    # Línea de la media
    plt.axvline(media)

    plt.title(f"Análisis {dimension}")
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia")

    print("\nANÁLISIS:")
    print(f"Media: {media}")
    print(f"Distancia promedio al origen: {media_distancia}")

    plt.show()