# models/walk_3d.py
# Simulación de caminata aleatoria en 3D.

def trayectoria_3d(num_saltos, rng):
    """Calcula la trayectoria en 3D para una caminata aleatoria.

    :param num_saltos: número de pasos a simular
    :param rng: generador pseudoaleatorio (GCL)
    :return: tupla de listas (x_vals, y_vals, z_vals) de posiciones
    """
    x, y, z = 0, 0, 0
    x_vals, y_vals, z_vals = [x], [y], [z]

    for _ in range(num_saltos):
        u = rng.next_float()

        # Direcciones posibles (+x, -x, +y, -y, +z, -z) con probabilidad 1/6
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

        x_vals.append(x)
        y_vals.append(y)
        z_vals.append(z)

    return x_vals, y_vals, z_vals