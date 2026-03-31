# generators/gcl.py
# Módulo que provee un RNG sencillo basado en el método congruencial lineal.

class GCL:
    """Generador Congruencial Lineal (LCG) usado por las caminatas.

    Ecuación de recurrencia:
        X(n+1) = (a * X(n) + c) mod m
    Variable uniforme:
        U(n) = X(n) / m
    """

    def __init__(self, seed: int, a: int, c: int, m: int):
        """Configura parámetros y estado inicial del generador.

        :param seed: valor inicial (semilla X0)
        :param a: multiplicador
        :param c: incremento
        :param m: módulo
        """
        # Parámetros del generador
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m
        # Estado interno actual (Xn)
        self.current = seed

    def next_int(self) -> int:
        """Avanza un paso y devuelve el siguiente número entero pseudoaleatorio."""
        self.current = (self.a * self.current + self.c) % self.m
        return self.current

    def next_float(self) -> float:
        """Devuelve el número pseudoaleatorio normalizado entre 0 y 1."""
        return round(self.next_int() / self.m, 5)

    def generate_sequence(self, n: int):
        """Genera secuencia de n números en [0,1] usando next_float."""
        return [self.next_float() for _ in range(n)]

    def reset(self):
        """Vuelve a la semilla inicial, útil para reproducibilidad."""
        self.current = self.seed