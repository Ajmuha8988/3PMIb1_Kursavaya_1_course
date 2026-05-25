import numpy as np
from numba import njit
# Библиотеки для работы с массивами и быстрыми вычислениями

def get_determinant(matrix):
    size = len(matrix)
    if size == 1:
        return matrix[0][0]
    if size == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    det = 0
    for col in range(size):
        minor = [row[:col] + row[col+1:] for row in matrix[1:]]
        det += ((-1) ** col) * matrix[0][col] * get_determinant(minor)
    return det
# Рекурсивное вычисление определителя для метода Крамера

def get_canonical_coeffs(x_data, y_data):
    n = len(x_data)
    matrix = [[float(x**i) for i in range(n)] for x in x_data]
    d_main = get_determinant(matrix)
    if abs(d_main) < 1e-12: return None
    
    coeffs = []
    for i in range(n):
        v_matrix = [row[:] for row in matrix]
        for j in range(n):
            v_matrix[j][i] = y_data[j]
        d_i = get_determinant(v_matrix)
        coeffs.append(d_i / d_main)
    return coeffs
# Получение коэффициентов канонического полинома

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
    
    coef = np.copy(y_s)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i-1]) / (x_s[i] - x_s[i-j])
            
    res = coef[0]
    prod = 1.0
    for k in range(1, n):
        prod *= (x_val - x_s[k-1])
        res += coef[k] * prod
        
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