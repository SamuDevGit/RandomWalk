# models/tests/mean_test.py

import math

class MeanTest:
    """
    Prueba de Medias para validar generadores de números pseudoaleatorios.
    Verifica si la media empírica de la secuencia es estadísticamente igual a 0.5.
    Diseñado con un nivel de confianza estricto del 95% (alpha = 0.05).
    """
    
    def __init__(self):
        # Nivel de significancia estandarizado para todo el proyecto (Alpha = 0.05).
        # Para pruebas de dos colas (limite inferior y superior), usamos Z_(alpha/2).
        # El valor Z correspondiente a 0.025 es una constante matemática: 1.96.
        self.z_alpha_half = 1.96
        self.theoretical_mean = 0.5
        
        # La varianza teórica de una distribución U(0,1) es 1/12.
        # Guardamos la raíz cuadrada (desviación estándar teórica) para optimizar cálculos.
        self.theoretical_std_dev = math.sqrt(1.0 / 12.0)

    def test(self, sequence: list[float]) -> dict:
        """
        Ejecuta la prueba de medias sobre la secuencia proporcionada.
        
        Args:
            sequence (list[float]): Lista de números pseudoaleatorios R_i en el intervalo (0,1).
            
        Returns:
            dict: Diccionario con los límites, estadísticos calculados y el veredicto final.
        """
        n = len(sequence)
        
        # 1. Validación de seguridad
        if n == 0:
            raise ValueError("La secuencia no puede estar vacía. No hay datos para evaluar.")
            
        # 2. Cálculo de la Media Empírica (promedio real de los datos generados)
        # sum() es nativo de Python y altamente optimizado en C.
        empirical_mean = sum(sequence) / n
        
        # 3. Cálculo del Error Estándar de la Media
        # Formula: Desviación_Estándar_Teórica / sqrt(n)
        standard_error = self.theoretical_std_dev / math.sqrt(n)
        
        # 4. Cálculo del Margen de Error
        # Formula: Z * Error_Estándar
        margin_of_error = self.z_alpha_half * standard_error
        
        # 5. Definición del Intervalo de Confianza (Límites de Aceptación)
        lower_limit = self.theoretical_mean - margin_of_error
        upper_limit = self.theoretical_mean + margin_of_error
        
        # 6. Veredicto: Evaluamos la Hipótesis Nula (H0)
        # H0: La media empírica == 0.5
        passed = lower_limit <= empirical_mean <= upper_limit
        
        # 7. (Opcional) Estadístico de Prueba Z_observado para el informe
        # Z_obs = (Media_Empírica - Media_Teórica) / Error_Estándar
        z_observed = (empirical_mean - self.theoretical_mean) / standard_error
        
        return {
            "test_name": "Prueba de Medias",
            "n": n,
            "empirical_mean": empirical_mean,
            "theoretical_mean": self.theoretical_mean,
            "confidence_level": 0.95,
            "z_critical": self.z_alpha_half,
            "z_observed": z_observed,
            "lower_limit": lower_limit,
            "upper_limit": upper_limit,
            "passed": passed,
            "status": "Aprobado (No se rechaza H0)" if passed else "Rechazado (Sesgo detectado)"
        }