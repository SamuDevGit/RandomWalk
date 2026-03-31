# models/tests/runs_test.py

import math

class RunsTest:
    """
    Prueba de Rachas (Runs Test) para evaluar la Independencia Secuencial.
    Verifica si el orden temporal de los números presenta tendencias no aleatorias,
    evaluando rachas por encima y por debajo de la mediana teórica (0.5).
    Nivel de confianza fijado al 95% (alpha = 0.05).
    """
    
    def __init__(self):
        self.theoretical_median = 0.5
        # Para prueba de dos colas con 95% de confianza, Z_critico = 1.96
        self.z_alpha_half = 1.96

    def test(self, sequence: list[float]) -> dict:
        """
        Ejecuta la prueba de rachas sobre la secuencia proporcionada.
        """
        n = len(sequence)
        
        if n < 2:
            raise ValueError("Se requieren al menos 2 números para evaluar rachas.")
            
        # 1. Asignación de signos (+ y -) respecto a la mediana teórica
        signs = []
        n1 = 0  # Contador de positivos
        n2 = 0  # Contador de negativos
        
        for r in sequence:
            if r >= self.theoretical_median:
                signs.append('+')
                n1 += 1
            else:
                signs.append('-')
                n2 += 1
                
        # Seguridad estadística: Si todos son de un mismo signo, falla automáticamente
        if n1 == 0 or n2 == 0:
            return {
                "test_name": "Prueba de Rachas",
                "passed": False,
                "status": "Rechazado (Generador degenerado, varianza cero)"
            }

        # 2. Conteo de Rachas (R) emulando el proceso manual
        R = 1 # La primera racha inicia con el primer signo
        for i in range(1, n):
            # Si el signo actual es diferente al anterior, es una nueva racha
            if signs[i] != signs[i - 1]:
                R += 1
                
        # 3. Cálculo de Parámetros Estadísticos
        # Media esperada (mu_R)
        mu_R = ((2.0 * n1 * n2) / n) + 1.0
        
        # Varianza matemática correcta (Wald-Wolfowitz)
        numerator = 2.0 * n1 * n2 * (2.0 * n1 * n2 - n)
        denominator = (n ** 2) * (n - 1)
        sigma2_R = numerator / denominator
        
        sigma_R = math.sqrt(sigma2_R)
        
        # 4. Cálculo del Estadístico Z
        z_observed = (R - mu_R) / sigma_R
        
        # 5. Veredicto (Prueba de dos colas)
        passed = abs(z_observed) <= self.z_alpha_half
        
        return {
            "test_name": "Prueba de Rachas (Independencia)",
            "n": n,
            "n1_positives": n1,
            "n2_negatives": n2,
            "total_runs_R": R,
            "expected_runs_mu": mu_R,
            "variance_sigma2": sigma2_R,
            "z_observed": z_observed,
            "z_critical": self.z_alpha_half,
            "passed": passed,
            "status": "Aprobado (Independencia secuencial)" if passed else "Rechazado (Tendencia detectada)",
            "signs_sequence": signs # Opcional: Para renderizar la lista de + y - en la UI
        }