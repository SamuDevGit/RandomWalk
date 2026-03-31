import matplotlib.pyplot as plt

def plot_1d(trayectoria):
    plt.figure()
    plt.plot(trayectoria)
    plt.title("Caminata 1D")
    plt.xlabel("Iteración")
    plt.ylabel("Posición")
    plt.grid()
    plt.show()