from generators.gcl import GCL
from models.walk_1d import caminata_1d
from config import A, C, M

def multiples_simulaciones(num_sim, num_saltos, seed):
    resultados = []

    for i in range(num_sim):
        rng = GCL(seed + i, A, C, M)
        resultados.append(caminata_1d(num_saltos, rng))

    return resultados