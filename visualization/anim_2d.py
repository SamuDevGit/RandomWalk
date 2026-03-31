import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# visualization/anim_2d.py
# Animación de caminata aleatoria en 2 dimensiones.

def animar_2d(num_saltos, rng):
    """Crea y muestra una animación de trayectoria 2D."""

    # Posición inicial en el origen
    x, y = 0, 0
    x_data, y_data = [x], [y]

    # Configuración básica de figura y objetos gráficos
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=1)
    punto, = ax.plot([], [], 'ro')

    ax.set_title("Animación Caminata 2D")

    def update(frame):
        """Actualiza posición y gráfico en cada paso de la animación."""
        nonlocal x, y

        u = rng.next_float()

        # 4 direcciones con probabilidad uniforme
        if u < 0.25:
            x += 1
        elif u < 0.5:
            x -= 1
        elif u < 0.75:
            y += 1
        else:
            y -= 1

        x_data.append(x)
        y_data.append(y)

        # Actualiza línea trazada y marcador del punto actual
        line.set_data(x_data, y_data)
        punto.set_data([x], [y])

        # Ajusta límites según rango de datos acumulados
        ax.set_xlim(min(x_data) - 5, max(x_data) + 5)
        ax.set_ylim(min(y_data) - 5, max(y_data) + 5)

        return line, punto

    # Ejecutar animación y mostrar gráfico con cuadrícula
    ani = FuncAnimation(fig, update, frames=num_saltos, interval=10, repeat=False)
    plt.grid()
    plt.show()