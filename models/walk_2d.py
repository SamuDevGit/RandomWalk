# models/walk_2d.py
# Simulación de caminata aleatoria en 2D.

def trayectoria_2d(num_saltos, rng):
    """Calcula la trayectoria 2D para una caminata aleatoria.

    :param num_saltos: cantidad de pasos
    :param rng: generador de números pseudoaleatorios (GCL)
    :return: tupla de listas (x_vals, y_vals) de posiciones en cada paso
    """
    x, y = 0, 0
    x_vals, y_vals = [x], [y]

    for _ in range(num_saltos):
        u = rng.next_float()

        # Se elige una dirección con probabilidad 1/4 cada una
        if u < 0.25:
            x += 1
        elif u < 0.5:
            x -= 1
        elif u < 0.75:
            y += 1
        else:
            y -= 1

        x_vals.append(x)
        y_vals.append(y)

    return x_vals, y_vals