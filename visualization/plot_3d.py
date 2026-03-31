import matplotlib.pyplot as plt

def plot_3d(x, y, z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(x, y, z)
    ax.scatter(0, 0, 0)
    ax.scatter(x[-1], y[-1], z[-1])

    ax.set_title("Caminata 3D")
    plt.show()