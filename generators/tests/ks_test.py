# models/tests/ks_test.py

import math

class KolmogorovSmirnovTest:
    """
    Prueba de Kolmogorov-Smirnov (KS) para evaluar la Uniformidad.
    Calcula la máxima divergencia (D_max) entre la Distribución Acumulada Empírica 
    y la Teórica Esperada U(0,1).
    Nivel de confianza fijado al 95% (alpha = 0.05).
    """
    
    def __init__(self):
        self.alpha = 0.05
        
        # Tabla de valores críticos (D_max_p) de Kolmogorov-Smirnov para alpha = 0.05
        # Clave: 'n' (cantidad de datos) | Valor: D Crítico
        # Para n > 35, se utiliza la fórmula de aproximación asintótica.
        self.ks_table = {
            1: 0.975, 2: 0.842, 3: 0.708, 4: 0.624, 5: 0.563,
            6: 0.519, 7: 0.483, 8: 0.454, 9: 0.430, 10: 0.409,
            11: 0.391, 12: 0.375, 13: 0.361, 14: 0.349, 15: 0.338,
            16: 0.327, 17: 0.318, 18: 0.309, 19: 0.301, 20: 0.294,
            21: 0.287, 22: 0.281, 23: 0.275, 24: 0.269, 25: 0.264,
            26: 0.259, 27: 0.254, 28: 0.250, 29: 0.246, 30: 0.242,
            31: 0.238, 32: 0.234, 33: 0.231, 34: 0.227, 35: 0.224
        }

    def test(self, sequence: list[float]) -> dict:
        """
        Ejecuta la prueba KS y genera la tabla agrupada para la UI.
        """
        n = len(sequence)
        
        if n == 0:
            raise ValueError("La secuencia no puede estar vacía.")
            
        # =================================================================
        # PARTE 1: CÁLCULO ESTRICTO DE D_MAX (Método Continuo Exacto)
        # =================================================================
        # sorted() es nativo de Python (usa Timsort O(n log n))
        sorted_seq = sorted(sequence)
        
        d_plus_max = 0.0
        d_minus_max = 0.0
        
        for i in range(n):
            # Probabilidad Empírica Acumulada: (i + 1) / n (Hasta este punto)
            # Probabilidad Teórica Acumulada para U(0,1): El valor del número mismo (sorted_seq[i])
            f_emp_upper = (i + 1) / n
            f_emp_lower = i / n
            r_i = sorted_seq[i]
            
            # Diferencia por encima (D+) y por debajo (D-) del escalón
            d_plus = f_emp_upper - r_i
            d_minus = r_i - f_emp_lower
            
            if d_plus > d_plus_max: d_plus_max = d_plus
            if d_minus > d_minus_max: d_minus_max = d_minus
                
        # El error máximo absoluto (El D_MAX del que habla el profesor)
        d_max_obs = max(d_plus_max, d_minus_max)
        
        # Obtener el D_MAX Crítico de la tabla (DMAXP)
        if n in self.ks_table:
            d_max_p = self.ks_table[n]
        else:
            # Fórmula asintótica de Smirnov para n > 35 y alpha = 0.05
            d_max_p = 1.36 / math.sqrt(n)
            
        passed = d_max_obs <= d_max_p

        # =================================================================
        # PARTE 2: RECREACIÓN DEL EXCEL DEL PROFESOR (Para la UI)
        # =================================================================
        # Esto agrupa los datos en 10 "canastos" idéntico al CSV subido.
        num_canastos = 10
        canastos = [0] * num_canastos
        
        for r in sequence:
            idx = int(r * num_canastos)
            if idx == num_canastos: idx -= 1
            canastos[idx] += 1
            
        excel_table = []
        acum_obt = 0
        acum_esp = 0
        
        for i in range(num_canastos):
            acum_obt += canastos[i]
            acum_esp += n / num_canastos # Si n=50, esto suma 5 cada vez
            
            p_obt = acum_obt / n
            p_esp = acum_esp / n
            diferencia = abs(p_obt - p_esp)
            
            excel_table.append({
                "canasto": i + 1,
                "frec_obt": canastos[i],            # Cuántos cayeron aquí
                "frec_acum_obt": acum_obt,          # Cuántos llevamos en total
                "p_obt": p_obt,                     # Frec. Acumulada / N
                "frec_esp_acum": acum_esp,          # Cuántos deberíamos llevar
                "p_esp": p_esp,                     # Probabilidad esperada
                "diferencia": diferencia            # Error en este canasto
            })

        return {
            "test_name": "Prueba Kolmogorov-Smirnov",
            "n": n,
            "d_max_observado": d_max_obs,
            "d_max_critico": d_max_p,
            "passed": passed,
            "status": "Aprobado (Distribución Uniforme)" if passed else "Rechazado",
            "excel_data": excel_table # Pasa esta lista directo a tu QTableWidget
        }