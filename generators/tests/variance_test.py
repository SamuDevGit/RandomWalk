# models/tests/variance_test.py

import math

class VarianceTest:
    """
    Prueba de Varianza para validar generadores de números pseudoaleatorios.
    Verifica si la dispersión de la secuencia es estadísticamente igual a 1/12,
    fijando un nivel de confianza estricto del 95% (alpha = 0.05).
    """
    
    def __init__(self):
        # Alpha = 0.05 fijado por requerimientos del proyecto.
        # Al ser una prueba de dos colas, usamos alpha/2 = 0.025.
        # El valor Z correspondiente en la Normal Estándar es 1.96.
        self.z_alpha_half = 1.96

    def test(self, sequence: list[float]) -> dict:
        """
        Ejecuta la prueba de varianza sobre la secuencia de números.
        
        Args:
            sequence (list[float]): Lista de números pseudoaleatorios R_i en (0,1).
            
        Returns:
            dict: Resultados y veredicto de la prueba.
        """
        n = len(sequence)
        
        if n <= 30:
            raise ValueError("La prueba de varianza requiere n > 30 para usar la aproximación de Wilson-Hilferty.")
            
        # 1. Calcular la media empírica (necesaria para la varianza)
        empirical_mean = sum(sequence) / n
        
        # 2. Calcular la Varianza Empírica (S^2)
        # S^2 = sum((R_i - media)^2) / (n - 1)
        sum_sq_diff = sum((x - empirical_mean) ** 2 for x in sequence)
        empirical_variance = sum_sq_diff / (n - 1)
        
        # 3. Grados de libertad (v)
        v = n - 1
        
        # 4. Aproximación de Wilson-Hilferty para Chi-Cuadrado (Limites invertidos por propiedad de Chi2)
        # Chi_cuadrado_superior (usa Z positivo)
        chi2_upper = v * (1.0 - (2.0 / (9.0 * v)) + self.z_alpha_half * math.sqrt(2.0 / (9.0 * v))) ** 3
        
        # Chi_cuadrado_inferior (usa Z negativo)
        chi2_lower = v * (1.0 - (2.0 / (9.0 * v)) - self.z_alpha_half * math.sqrt(2.0 / (9.0 * v))) ** 3
        
        # 5. Calcular los límites de aceptación para la varianza
        # Denominador de la fórmula: 12 * (n - 1)
        denominator = 12.0 * v
        
        lower_limit = chi2_lower / denominator
        upper_limit = chi2_upper / denominator
        
        # 6. Veredicto: ¿La varianza empírica cae dentro de los límites?
        passed = lower_limit <= empirical_variance <= upper_limit
        
        return {
            "test_name": "Prueba de Varianza",
            "n": n,
            "empirical_variance": empirical_variance,
            "theoretical_variance": 1.0 / 12.0,
            "confidence_level": 0.95,
            "chi2_lower_approx": chi2_lower,
            "chi2_upper_approx": chi2_upper,
            "lower_limit": lower_limit,
            "upper_limit": upper_limit,
            "passed": passed,
            "status": "Aprobado" if passed else "Rechazado"
        }