import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# visualization/anim_3d.py
# Animación de caminata aleatoria en tres dimensiones.

def animar_3d(num_saltos, rng):
    """Crea y muestra animación 3D de la trayectoria aleatoria."""

    # Importación local requerida para ax.plot en 3D
    from mpl_toolkits.mplot3d import Axes3D

    # Posición inicial en el origen
    x, y, z = 0, 0, 0
    x_data, y_data, z_data = [x], [y], [z]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    line, = ax.plot([], [], [], lw=1)
    punto = ax.scatter([x], [y], [z], color='red')

    ax.set_title("Animación Caminata 3D")

    def update(frame):
        """Actualiza la posición en 3D y redibuja línea + marcador."""
        nonlocal x, y, z, punto

        u = rng.next_float()

        # Seis direcciones equivalentes
        if u < 1/6:
            x += 1
        elif u < 2/6:
            x -= 1
        elif u < 3/6:
            y += 1
        elif u < 4/6:
            y -= 1
        elif u < 5/6:
            z += 1
        else:
            z -= 1

        x_data.append(x)
        y_data.append(y)
        z_data.append(z)

        # Actualiza trayectoria 3D y puntos
        line.set_data(x_data, y_data)
        line.set_3d_properties(z_data)

        punto.remove()
        punto = ax.scatter([x], [y], [z], color='red')

        # Ajuste dinámico de límites
        ax.set_xlim(min(x_data) - 5, max(x_data) + 5)
        ax.set_ylim(min(y_data) - 5, max(y_data) + 5)
        ax.set_zlim(min(z_data) - 5, max(z_data) + 5)

        return line,

    # Lanza animación.
    ani = FuncAnimation(fig, update, frames=num_saltos, interval=10, repeat=False)
    plt.show()