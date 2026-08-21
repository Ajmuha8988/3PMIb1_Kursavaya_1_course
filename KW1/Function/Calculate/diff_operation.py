import math
# Импорт математической библиотеки

from Function.Calculate.CLAY import (solve_gauss, solve_cramer, solve_matrix, 
                                     solve_thomas)
# Импорт методов решения СЛАУ

def eval_expr(expr, x):
    allowed_names = {
        'x': x,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'exp': math.exp,
        'log': math.log,
        'pi': math.pi,
        'e': math.e,
        'sqrt': math.sqrt,
        'abs': abs
    }
    safe_expr = expr.replace('^', '**')
    return eval(safe_expr, {"__builtins__": None}, allowed_names)
# Функция безопасного вычисления математического выражения

def solve_bvp(p_str, q_str, f_str, x_start, y_start, x_end, y_end, n, 
              method='thomas'):
    h = (x_end - x_start) / n
    x_grid = [x_start + i * h for i in range(n + 1)]
    
    A_coefs = []
    C_coefs = []
    B_coefs = []
    D_coefs = []
    
    for i in range(1, n):
        xi = x_grid[i]
        pi = eval_expr(p_str, xi)
        qi = eval_expr(q_str, xi)
        fi = eval_expr(f_str, xi)
        
        ai = 1.0 - (h / 2.0) * pi
        ci = -2.0 + (h ** 2) * qi
        bi = 1.0 + (h / 2.0) * pi
        di = (h ** 2) * fi
        
        A_coefs.append(ai)
        C_coefs.append(ci)
        B_coefs.append(bi)
        D_coefs.append(di)
        
    D_coefs[0] -= A_coefs[0] * y_start
    D_coefs[-1] -= B_coefs[-1] * y_end
    
    size = n - 1
    
    if method == 'thomas':
        a_list = [0.0] + A_coefs[1:]
        c_list = C_coefs
        b_list = B_coefs[:-1] + [0.0]
        y_inner = solve_thomas(a_list, c_list, b_list, D_coefs)
        
    else:
        M = [[0.0] * size for _ in range(size)]
        for i in range(size):
            M[i][i] = C_coefs[i]
            if i > 0:
                M[i][i-1] = A_coefs[i]
            if i < size - 1:
                M[i][i+1] = B_coefs[i]
                
        if method == 'gauss':
            y_inner = solve_gauss(M, D_coefs)
        elif method == 'matrix':
            y_inner = solve_matrix(M, D_coefs)
        elif method == 'cramer':
            if size > 11:
                raise ValueError("Метод Крамера не применим для n > 11.")
            y_inner = solve_cramer(M, D_coefs)
        else:
            raise ValueError("Неподдерживаемый метод решения.")
            
    return x_grid, [y_start] + y_inner + [y_end]
# Решение краевой задачи методом конечных разностей