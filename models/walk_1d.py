# models/walk_1d.py
# Funcionalidad de caminata aleatoria en una dimensión.


def caminata_1d(num_saltos, rng):
    """Ejecuta una caminata 1D y devuelve la posición final.

    :param num_saltos: cantidad de pasos a simular
    :param rng: generador de números pseudoaleatorios (clase GCL)
    :return: posición final después de num_saltos movimientos
    """
    posicion = 0

    for _ in range(num_saltos):
        u = rng.next_float()
        # Paso +1 o -1 con probabilidad 0.5 cada uno
        posicion += 1 if u < 0.5 else -1

    return posicion


def trayectoria_1d(num_saltos, rng):
    """Devuelve la lista de posiciones en cada paso de la caminata 1D."""
    posicion = 0
    trayectoria = [posicion]

    for _ in range(num_saltos):
        u = rng.next_float()
        posicion += 1 if u < 0.5 else -1
        trayectoria.append(posicion)

    return trayectoria