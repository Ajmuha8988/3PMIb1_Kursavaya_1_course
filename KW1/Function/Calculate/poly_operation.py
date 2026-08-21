import math
import numpy as np
# Библиотеки для работы с массивами и быстрыми вычислениями

from Function.Calculate.CLAY import get_determinant
# Рекурсивное вычисление определителя для метода Крамера

from Function.Calculate.CLAY import get_determinant, solve_gauss
# Рекурсивное вычисление определителя для метода Крамера и метод Гаусса как резервный/устойчивый метод

def get_canonical_coeffs(x_data, y_data):
    n = len(x_data)
    
    if n > 6:
        try:
            matrix = [[float(x**i) for i in range(n)] for x in x_data]
            return solve_gauss(matrix, list(y_data))
        except Exception:
            return None

    matrix = [[float(x**i) for i in range(n)] for x in x_data]
    d_main = get_determinant(matrix)
    
    if abs(d_main) < 1e-30: 
        try:
            return solve_gauss(matrix, list(y_data))
        except Exception:
            return None
    
    coeffs = []
    for i in range(n):
        v_matrix = [row[:] for row in matrix]
        for j in range(n):
            v_matrix[j][i] = y_data[j]
        d_i = get_determinant(v_matrix)
        coeffs.append(d_i / d_main)
    return coeffs
# Получение коэффициентов канонического полинома с автоматическим выбором метода

def poly_lagrange(x_val, x_data, y_data):
    n = len(x_data)
    res = 0
    for i in range(n):
        basis = 1
        for j in range(n):
            if i != j:
                basis *= (x_val - x_data[j]) / (x_data[i] - x_data[j])
        res += y_data[i] * basis
    return res
# Полином Лагранжа

def poly_newton(x_val, x_data, y_data):
    n = len(x_data)
    if n < 1: return 0.0
    if n == 1: return y_data[0]
    
    idx = np.argsort(x_data)
    x_s = x_data[idx].astype(float)
    y_s = y_data[idx].astype(float)
    
    h = x_s[1] - x_s[0]
    tolerance = 1e-9 
    for i in range(1, n - 1):
        current_step = x_s[i+1] - x_s[i]
        if abs(current_step - h) > tolerance:
            raise ValueError("Узлы не являются равноотстоящими")
            
    dy = np.zeros((n, n))
    dy[:, 0] = y_s
    
    for j in range(1, n):
        for i in range(n - j):
            dy[i, j] = dy[i+1, j-1] - dy[i, j-1]
            
    q = (x_val - x_s[0]) / h
    res = dy[0, 0]
    
    term = 1.0
    for k in range(1, n):
        term *= (q - k + 1)
        res += (term * dy[0, k]) / math.factorial(k)
        
    return res
# Полином Ньютона

def format_universal_formula(coeffs):
    if not coeffs: return ""
    terms = []
    for i, c in enumerate(coeffs):
        if abs(c) < 1e-4: continue
        sign = "+" if c >= 0 and i > 0 else ""
        term = f"{sign}{c:.3f}"
        if i > 0: term += f"x^{i}" if i > 1 else "x"
        terms.append(term)
    return "P(n) = " + " ".join(terms)
# Формирование строки с универсальной формулой полинома