# models/tests/poker_test.py

import math

class PokerTest:
    """
    Prueba de Póker para evaluar la Independencia de los números pseudoaleatorios.
    Analiza los primeros 5 decimales simulando manos de póker y evalúa
    la frecuencia mediante la distribución Chi-Cuadrado (alpha = 0.05).
    """
    
    def __init__(self):
        self.alpha = 0.05
        
        # Probabilidades teóricas de cada mano para 5 decimales
        self.probabilities = {
            "TD": 0.3024,  # Todos Diferentes
            "1P": 0.5040,  # Un Par
            "2P": 0.1080,  # Dos Pares
            "T":  0.0720,  # Tercia
            "FH": 0.0090,  # Full House
            "P":  0.0045,  # Póker
            "Q":  0.0001   # Quintilla
        }
        
        # Diccionario para traducir "firmas" de repetición a manos de póker
        self.hand_signatures = {
            (1, 1, 1, 1, 1): "TD",
            (2, 1, 1, 1):    "1P",
            (2, 2, 1):       "2P",
            (3, 1, 1):       "T",
            (3, 2):          "FH",
            (4, 1):          "P",
            (5,):            "Q"
        }
        
        # Valores críticos de Chi-Cuadrado para alpha = 0.05 (Una cola)
        self.chi2_table = {
            1: 3.841, 2: 5.991, 3: 7.815, 4: 9.488, 5: 11.070, 6: 12.592, 7: 14.067
        }
        self.z_alpha = 1.645

    def _classify_hand(self, r_i: float) -> str:
        """
        Toma un número R_i, extrae 5 decimales y devuelve la mano de Póker.
        """
        # 1. Convertir a string, forzar 5 decimales fijos (ej. 0.1 -> "0.10000")
        # y omitir el "0." tomando desde el índice 2
        decimals_str = f"{r_i:.5f}"[2:7]
        
        # 2. Contar frecuencias de cada dígito manualmente (Sin usar collections.Counter)
        counts_dict = {}
        for char in decimals_str:
            counts_dict[char] = counts_dict.get(char, 0) + 1
            
        # 3. Extraer los valores, ordenarlos de mayor a menor y convertirlos a tupla
        signature = tuple(sorted(counts_dict.values(), reverse=True))
        
        # 4. Retornar la mano que corresponda a la firma
        return self.hand_signatures[signature]

    def test(self, sequence: list[float]) -> dict:
        """
        Ejecuta la Prueba de Póker sobre toda la secuencia.
        """
        n = len(sequence)
        if n == 0:
            raise ValueError("La secuencia no puede estar vacía.")
            
        # 1. Inicializar contadores de Frecuencias Observadas (FO)
        observed_freqs = {hand: 0 for hand in self.probabilities.keys()}
        
        # 2. Clasificar cada número de la secuencia
        for r in sequence:
            hand = self._classify_hand(r)
            observed_freqs[hand] += 1
            
        # 3. Calcular el Estadístico Chi-Cuadrado Observado
        chi2_observed = 0.0
        expected_freqs = {}
        table_data = [] # Para que tu interfaz gráfica renderice la tabla
        
        for hand, prob in self.probabilities.items():
            expected = n * prob
            expected_freqs[hand] = expected
            observed = observed_freqs[hand]
            
            # Cálculo parcial de Chi-Cuadrado para esta mano
            # Nota: Si expected es 0 (imposible matemáticamente aquí, pero buena práctica), lo protegemos.
            if expected > 0:
                chi_partial = ((observed - expected) ** 2) / expected
                chi2_observed += chi_partial
            else:
                chi_partial = 0.0
                
            # Guardamos la fila para la tabla de la UI
            table_data.append({
                "mano": hand,
                "probabilidad": prob,
                "fo": observed,
                "fe": expected,
                "chi_parcial": chi_partial
            })
            
        # 4. Determinar los Grados de Libertad (v = k - 1)
        # k es la cantidad de categorías (7 manos)
        v = len(self.probabilities) - 1
        
        # 5. Obtener el Valor Crítico de Chi-Cuadrado
        if v in self.chi2_table:
            chi2_critical = self.chi2_table[v]
        else:
            chi2_critical = v * (1.0 - (2.0 / (9.0 * v)) + self.z_alpha * math.sqrt(2.0 / (9.0 * v))) ** 3
            
        # 6. Veredicto: Al igual que la Uniformidad, esto se evalúa con una cola superior.
        passed = chi2_observed <= chi2_critical
        
        return {
            "test_name": "Prueba de Póker (5 Decimales)",
            "n": n,
            "degrees_of_freedom": v,
            "chi2_observed": chi2_observed,
            "chi2_critical": chi2_critical,
            "passed": passed,
            "status": "Aprobado (Dígitos Independientes)" if passed else "Rechazado (Patrones Detectados)",
            "table_data": table_data
        }