from generators.gcl import GCL
from models.walk_2d import trayectoria_2d
from config import A, C, M

def multiples_simulaciones_2d(num_sim, num_saltos, seed):
    resultados_x = []
    resultados_y = []

    for i in range(num_sim):
        rng = GCL(seed + i, A, C, M)
        x, y = trayectoria_2d(num_saltos, rng)

        resultados_x.append(x[-1])  # posición final
        resultados_y.append(y[-1])

    return resultados_x, resultados_y