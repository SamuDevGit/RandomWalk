import matplotlib.pyplot as plt

def scatter_2d(x, y):
    plt.figure()
    plt.scatter(x, y)
    plt.title("Posiciones finales - Caminata 2D")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid()
    plt.show()