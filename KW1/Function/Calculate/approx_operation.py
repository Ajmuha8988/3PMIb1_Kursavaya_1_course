from Function.Calculate.CLAY import solve_gauss
# Импорт метода решения СЛАУ

def fit_linear(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x2 = sum(xi**2 for xi in x)
    sum_xy = sum(x[i] * y[i] for i in range(n))

    A = [
        [sum_x2, sum_x],
        [sum_x, n]
    ]
    B = [sum_xy, sum_y]
    
    coeffs = solve_gauss(A, B)
    a, b = coeffs[0], coeffs[1]
    sse = sum((y[i] - (a * x[i] + b))**2 for i in range(n))
    return a, b, sse
# Расчет коэффициентов линейной регрессии

def fit_quadratic(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_x2 = sum(xi**2 for xi in x)
    sum_x3 = sum(xi**3 for xi in x)
    sum_x4 = sum(xi**4 for xi in x)
    sum_y = sum(y)
    sum_xy = sum(x[i] * y[i] for i in range(n))
    sum_x2y = sum((x[i]**2) * y[i] for i in range(n))

    A = [
        [sum_x4, sum_x3, sum_x2],
        [sum_x3, sum_x2, sum_x],
        [sum_x2, sum_x, n]
    ]
    B = [sum_x2y, sum_xy, sum_y]
    
    coeffs = solve_gauss(A, B)
    a, b, c = coeffs[0], coeffs[1], coeffs[2]
    sse = sum((y[i] - (a * (x[i]**2) + b * x[i] + c))**2 for i in range(n))
    return a, b, c, sse
# Расчет коэффициентов квадратичной регрессии

def fit_custom(x, y):
    n = len(x)
    if any(xi == 0 for xi in x):
        raise ValueError("Обнаружен x = 0. Пользовательская регрессия \
 y = a/x^2 + b/x + c не может быть рассчитана.")
        
    term1 = [1.0 / (xi**2) for xi in x]
    term2 = [1.0 / xi for xi in x]
    
    sum_t1_sq = sum(t**2 for t in term1)
    sum_t1_t2 = sum(term1[i] * term2[i] for i in range(n))
    sum_t1 = sum(term1)
    sum_t2_sq = sum(t**2 for t in term2)
    sum_t2 = sum(term2)
    
    sum_y_t1 = sum(y[i] * term1[i] for i in range(n))
    sum_y_t2 = sum(y[i] * term2[i] for i in range(n))
    sum_y = sum(y)
    
    A = [
        [sum_t1_sq, sum_t1_t2, sum_t1],
        [sum_t1_t2, sum_t2_sq, sum_t2],
        [sum_t1, sum_t2, n]
    ]
    B = [sum_y_t1, sum_y_t2, sum_y]
    
    coeffs = solve_gauss(A, B)
    a, b, c = coeffs[0], coeffs[1], coeffs[2]
    sse = sum((y[i] - (a / (x[i]**2) + b / x[i] + c))**2 for i in range(n))
    return a, b, c, sse
# Расчет коэффициентов пользовательской регрессии y = a/x^2 + b/x + c