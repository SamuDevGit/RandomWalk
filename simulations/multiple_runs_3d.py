from generators.gcl import GCL
from models.walk_3d import trayectoria_3d
from config import A, C, M

def multiples_simulaciones_3d(num_sim, num_saltos, seed):
    resultados_x = []
    resultados_y = []
    resultados_z = []

    for i in range(num_sim):
        rng = GCL(seed + i, A, C, M)
        x, y, z = trayectoria_3d(num_saltos, rng)

        resultados_x.append(x[-1])
        resultados_y.append(y[-1])
        resultados_z.append(z[-1])

    return resultados_x, resultados_y, resultados_z