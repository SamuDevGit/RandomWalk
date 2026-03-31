# models/tests/chi_square.py

import math

class ChiSquareTest:
    """
    Prueba de Chi-Cuadrado de Bondad de Ajuste para evaluar la Uniformidad.
    Verifica si los números generados se distribuyen equitativamente en k sub-intervalos.
    Nivel de confianza fijado al 95% (alpha = 0.05).
    """
    
    def __init__(self):
        self.alpha = 0.05
        
        # Para bondad de ajuste (una cola, 95% a la izquierda, 5% a la derecha), 
        # el Z correspondiente es 1.645
        self.z_alpha = 1.645
        
        # Tabla precalculada de valores críticos de Chi-Cuadrado para alpha = 0.05
        # Clave: Grados de libertad (v) | Valor: Chi-Cuadrado Crítico
        # Esto cubre los casos de uso más comunes en interfaces gráficas (hasta 21 intervalos)
        self.chi2_table = {
            1: 3.841,  2: 5.991,  3: 7.815,  4: 9.488,  5: 11.070,
            6: 12.592, 7: 14.067, 8: 15.507, 9: 16.919, 10: 18.307,
            11: 19.675, 12: 21.026, 13: 22.362, 14: 23.685, 15: 24.996,
            16: 26.296, 17: 27.587, 18: 28.869, 19: 30.144, 20: 31.410
        }

    def test(self, sequence: list[float], num_intervals: int = 10) -> dict:
        """
        Ejecuta la prueba Chi-Cuadrado sobre la secuencia.
        
        Args:
            sequence (list[float]): Lista de números R_i en [0,1).
            num_intervals (int): Cantidad de sub-intervalos 'k'. Por defecto 10.
            
        Returns:
            dict: Resultados completos, incluyendo arreglos de frecuencias para graficar.
        """
        n = len(sequence)
        
        if n == 0:
            raise ValueError("La secuencia no puede estar vacía.")
            
        # Condición estadística clásica: La frecuencia esperada debe ser >= 5
        expected_freq = n / num_intervals
        if expected_freq < 5:
            raise ValueError(f"Para {n} números, usar {num_intervals} intervalos da una frecuencia esperada de {expected_freq}. Debe ser >= 5. Reduce los intervalos o genera más números.")
            
        # 1. Inicializar contadores de Frecuencias Observadas
        observed_freqs = [0] * num_intervals
        
        # 2. Clasificar cada número en su intervalo correspondiente
        # Un método ultra rápido (O(N)): multiplicar el número por k y truncar al entero.
        # Ejemplo: R_i = 0.73, k = 10 -> int(7.3) = 7 (Cae en el índice 7)
        for r in sequence:
            index = int(r * num_intervals)
            # Protección por si el generador arroja exactamente 1.0
            if index == num_intervals:
                index = num_intervals - 1
            observed_freqs[index] += 1
            
        # 3. Calcular el Estadístico Chi-Cuadrado Observado
        chi2_observed = 0.0
        for observed in observed_freqs:
            chi2_observed += ((observed - expected_freq) ** 2) / expected_freq
            
        # 4. Determinar los Grados de Libertad (v = k - 1)
        v = num_intervals - 1
        
        # 5. Obtener el Valor Crítico de Chi-Cuadrado (Límite de Aceptación)
        if v in self.chi2_table:
            chi2_critical = self.chi2_table[v]
        else:
            # Plan de contingencia: Aproximación de Wilson-Hilferty para v > 20
            chi2_critical = v * (1.0 - (2.0 / (9.0 * v)) + self.z_alpha * math.sqrt(2.0 / (9.0 * v))) ** 3
            
        # 6. Veredicto (Prueba de una cola superior)
        # H0: Los datos son uniformes. (Se aprueba si chi2_obs <= chi2_crit)
        passed = chi2_observed <= chi2_critical
        
        return {
            "test_name": "Prueba Chi-Cuadrado (Uniformidad)",
            "n": n,
            "num_intervals": num_intervals,
            "degrees_of_freedom": v,
            "expected_frequency": expected_freq,
            "observed_frequencies": observed_freqs, # <--- ¡ORO PARA TU UI!
            "chi2_observed": chi2_observed,
            "chi2_critical": chi2_critical,
            "passed": passed,
            "status": "Aprobado (Distribución Uniforme)" if passed else "Rechazado (No es Uniforme)"
        }