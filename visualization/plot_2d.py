import matplotlib.pyplot as plt

def plot_2d(x_vals, y_vals):
    plt.figure()
    plt.plot(x_vals, y_vals)
    plt.scatter(0, 0)
    plt.scatter(x_vals[-1], y_vals[-1])
    plt.title("Caminata 2D")
    plt.axis("equal")
    plt.grid()
    plt.show()