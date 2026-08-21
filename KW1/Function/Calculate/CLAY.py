import numpy as np
from numba import njit

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
# Рекурсивное вычисление определителя матрицы.

def solve_gauss(A, B):
    n = len(B)
    M = [A[i] + [B[i]] for i in range(n)]
    
    for i in range(n):
        max_row = i
        for r in range(i + 1, n):
            if abs(M[r][i]) > abs(M[max_row][i]):
                max_row = r
        M[i], M[max_row] = M[max_row], M[i]

        if abs(M[i][i]) < 1e-12:
            raise ArithmeticError("Система не имеет однозначного решения.")
            
        pivot = M[i][i]
        for c in range(i, n + 1):
            M[i][c] /= pivot

        for r in range(n):
            if r != i:
                factor = M[r][i]
                for c in range(i, n + 1):
                    M[r][c] -= factor * M[i][c]
                    
    return [M[i][n] for i in range(n)]
# Функция для решения СЛАУ методом Гаусса

def solve_cramer(A, B):
    n = len(B)
    d_main = get_determinant(A)
    if abs(d_main) < 1e-12:
        raise ArithmeticError("Система не имеет однозначного решения.")
    
    coeffs = []
    for i in range(n):
        v_matrix = [row[:] for row in A]
        for j in range(n):
            v_matrix[j][i] = B[j]
        d_i = get_determinant(v_matrix)
        coeffs.append(d_i / d_main)
    return coeffs
# Функция для решения СЛАУ методом Крамера

def solve_matrix(A, B):
    n = len(B)
    inv = [[1.0 if j == i else 0.0 for j in range(n)] for i in range(n)]
    M = [A[i][:] for i in range(n)]
    for i in range(n):
        max_row = i
        for r in range(i + 1, n):
            if abs(M[r][i]) > abs(M[max_row][i]):
                max_row = r
        M[i], M[max_row] = M[max_row], M[i]
        inv[i], inv[max_row] = inv[max_row], inv[i]
        if abs(M[i][i]) < 1e-12:
            raise ArithmeticError("Матрица вырождена.")
        pivot = M[i][i]
        for c in range(n):
            M[i][c] /= pivot
            inv[i][c] /= pivot
        for r in range(n):
            if r != i:
                factor = M[r][i]
                for c in range(n):
                    M[r][c] -= factor * M[i][c]
                    inv[r][c] -= factor * inv[i][c]
    return [sum(inv[i][j] * B[j] for j in range(n)) for i in range(n)]
# Функция для решения СЛАУ матричным способом

@njit
def solve_thomas(a, c, b, d):
    n = len(d)
    alpha = [0.0] * (n + 1)
    beta = [0.0] * (n + 1)
    
    for i in range(n):
        denom = c[i] + a[i] * alpha[i]
        if abs(denom) < 1e-12:
            raise ArithmeticError("Деление на ноль в методе прогонки. \
 Нарушено условие устойчивости.")
        alpha[i+1] = -b[i] / denom
        beta[i+1] = (d[i] - a[i] * beta[i]) / denom
        
    y = [0.0] * n
    y[n-1] = beta[n]
    for i in range(n - 2, -1, -1):
        y[i] = alpha[i+1] * y[i+1] + beta[i+1]
    return y
# Метод прогонки для трехдиагональной СЛАУ