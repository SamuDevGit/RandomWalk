import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# visualization/anim_1d.py
# Animación de una caminata aleatoria unidimensional.

def animar_1d(num_saltos, rng):
    """Crea y muestra una animación de la trayectoria 1D paso a paso."""

    # Datos de la línea de tiempo
    x_data = []
    y_data = []

    # Posición inicial en 0
    posicion = 0

    # Configura la figura y el objeto de la línea animada
    fig, ax = plt.subplots()
    line, = ax.plot([], [])

    # Límites del gráfico (deberían ajustarse según promedio de salto)
    ax.set_xlim(0, num_saltos)
    ax.set_ylim(-100, 100)

    ax.set_title("Animación Caminata 1D")
    ax.set_xlabel("Paso")
    ax.set_ylabel("Posición")

    def update(frame):
        """Función llamada en cada frame para avanzar un paso y redibujar."""
        nonlocal posicion

        u = rng.next_float()

        # Paso aleatorio hacia adelante o atrás
        if u < 0.5:
            posicion += 1
        else:
            posicion -= 1

        x_data.append(frame)
        y_data.append(posicion)

        line.set_data(x_data, y_data)
        return line,

    # Inicia la animación (num_saltos frames, intervalo en ms entre frames)
    ani = FuncAnimation(fig, update, frames=num_saltos, interval=1, repeat=False)
    plt.show()