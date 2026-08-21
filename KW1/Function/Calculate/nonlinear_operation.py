import numpy as np
from numba import njit
# Библиотеки для работы с массивами и быстрыми вычислениями

from PyQt6.QtWidgets import (QMessageBox)
# Импорт компонентов библиотеки PyQt6 для работы с графическим интерфейсом

from Class.Components.tooltip import ModernHint as MH
# Импорт класса всплывающей подсказки

@njit(fastmath=True, cache=True)
def f_core(x, func_idx):
    if func_idx == 1:
        return 3.0**x + 2.0*x - 5.0
    elif func_idx == 2:
        return x**4 - 4.0*x**3 - 8.0*x**2 + 1.0
    elif func_idx == 3:
        return x**2 - 3.0 + 0.5**x
    else:
        if x <= -11: return np.nan
        return ((x - 2.0)**2) * np.log10(x + 11.0) - 1.0
# Функция-ядро для максимально быстрого вычисления математических формул

@njit(fastmath=True, cache=True)
def df_core(x, func_idx):
    if func_idx == 1:
        return 3.0**x * np.log(3.0) + 2.0
    elif func_idx == 2:
        return 4.0*x**3 - 12.0*x**2 - 16.0*x
    elif func_idx == 3:
        return 2.0*x + (0.5**x) * np.log(0.5)
    else:
        if x <= -11: return np.nan
        ln10 = np.log(10.0)
        return 2.0*(x - 2.0)*np.log10(x + 11.0) + ((x - 2.0)**2) / \
            ((x + 11.0) * ln10)
# Функция-ядро для вычисления производных

@njit(fastmath=True)
def bisection_method(func_idx, a, b, eps):
    fa = f_core(a, func_idx)
    iters = 0
    while (b - a) > eps / 2:
        c = (a + b) / 2
        fc = f_core(c, func_idx)
        if abs(fc) < 1e-15:
            if iters == 0:
                return c, iters + 1
            else:
                return c, iters
        if fa * fc < 0: b = c
        else:
            a = c
            fa = fc
        iters += 1
    return (a + b) / 2, iters
# Функция, реализующая алгоритм метода дихотомии

@njit(fastmath=True)
def chord_method(func_idx, a, b, eps):
    x_a = a
    x_b = b
    fx_a = f_core(a, func_idx)
    fx_b = f_core(b, func_idx)
    iters = 0
    x_curr, x_next = 0, 0
    while iters < 1000:
        x_curr = x_b - ((fx_b*(x_b-x_a))/(fx_b-fx_a))
        fx_curr = f_core(x_curr, func_idx)
        if fx_a * fx_curr > 0:
            x_a = x_curr
            fx_a = f_core(x_a, func_idx)
            x_next = x_b - ((fx_b*(x_b-x_a))/(fx_b-fx_a))
        else:
            x_b = x_curr
            fx_b = f_core(x_b, func_idx)
            x_next = x_b - ((fx_b*(x_b-x_a))/(fx_b-fx_a))
        if abs(x_next - x_curr) < eps / 2:
            if iters == 0:
                return x_curr, iters+1
            else:
                return x_curr, iters
        iters += 1
    return x_curr, iters
# Функция, реализующая алгоритм метода хорд

@njit(fastmath=True)
def tangent_method(func_idx, a, b, eps):
    x_curr = (a+b)/2
    iters = 0
    while iters < 1000:
        fx = f_core(x_curr, func_idx)
        dfx = df_core(x_curr, func_idx)
        h = fx / dfx
        x_next = x_curr - h
        if abs(x_next - x_curr) < eps / 2:
            if iters == 0:
                return x_curr, iters+1
            else:
                return x_curr, iters
        x_curr = x_next
        iters += 1
    return x_curr, iters
# Функция, реализующая алгоритм метода касательных

def combined_method(func_idx, a, b, eps):
    x_a = a
    x_b = b
    x = 0
    iters = 0
    while iters < 1000:
        fa = f_core(x_a, func_idx)
        fb = f_core(x_b, func_idx)
        dfb = df_core(x_b, func_idx)
        if abs(x_b - x_a) < eps / 2:
            x = (x_a + x_b)/2
            if iters == 0:
                return x, iters+1
            else:
                return x, iters
        x_a = x_a - ((fa * (x_b - x_a))/ (fb - fa))
        x_b = x_b - fb / dfb
        iters += 1
    return x, iters
# Функция, реализующая алгоритм комбинированного метода

@njit(fastmath=True)
def iter_method(func_idx, a, b, eps):
    dfa, dfb = df_core(a, func_idx), df_core(b, func_idx)
    M = max(dfa, dfb)
    m = min(dfa, dfb)
    k = 1.0 / M
    q = 1 - (m/M)
    x_curr = (a + b)/2
    if q < 1 and q >= 0:
        for i in range(1000):
            fx = f_core(x_curr, func_idx)
            x_next = x_curr - k * fx
            if abs(x_next - x_curr) < eps / 2:
                if i == 0:
                    return x_next, i+1
                else:
                    return x_next, i
            x_curr = x_next
        return x_curr, 1000
    else:
        M = max(-dfa, -dfb)
        k = 1/M
        for i in range(1000):
            fx = -(f_core(x_curr, func_idx))
            x_next = x_curr - k * fx
            if abs(x_next - x_curr) < eps / 2:
                if i == 0:
                    return x_next, i+1
                else:
                    return x_next, i
            x_curr = x_next
        return x_curr, 1000
# Функция, отвечающая за вычисления с помощью метода итерации

@njit(fastmath=True)
def find_b_logic(func_idx, a):
    step = 0.4
    val_a = f_core(a, func_idx)
    df_a = df_core(a, func_idx)
    for i in range(1, 500):
        for direction in [1.0, -1.0]:
            b_cand = a + i * step * direction
            val_b = f_core(b_cand, func_idx)
            df_b = df_core(b_cand, func_idx)
            if not np.isnan(val_b) and not np.isnan(df_b):
                if (val_a * val_b < 0) and (df_a * df_b > 0):
                    return b_cand
    return np.nan
# Функция, отвечающая за автоматический поиск подходящей границы b

def val_a_and_b(self):
    MH(self, "Знаки функции на краях должны быть разными", self.input_a)
# Функция, отвечающая за валидацию поля a и b

def clear_ui(self):
    for field in [self.res_dih, self.res_hor, self.res_kac, 
                  self.res_comba, self.res_iter, 
                  self.step_dih, self.step_hor, self.step_kac, 
                  self.step_comba, self.step_iter]:
        field.clear()
    self.ax.clear()
    self.canvas.draw()
# Функция, отвечающая за очистку графика и всех полей

def run_calculation(self):
    clear_ui(self)
    a = float(self.input_a.text().replace(',', '.'))
    b = float(self.input_b.text().replace(',', '.'))
    eps = float(self.input_e.text().replace(',', '.'))
    f_idx = 1
    if self.radio2.isChecked(): f_idx = 2
    elif self.radio3.isChecked(): f_idx = 3
    elif self.radio4.isChecked(): f_idx = 4

    r_dih, i_dih = bisection_method(f_idx, a, b, eps)
    r_hor, i_hor = chord_method(f_idx, a, b, eps)
    r_kac, i_kac = tangent_method(f_idx, a, b, eps) 
    r_com, i_com = combined_method(f_idx, a, b, eps)
    r_ite, i_ite = iter_method(f_idx, a, b, eps)

    self.res_dih.setText(f"{r_dih:.8}"); 
    self.step_dih.setText(str(i_dih ))
    self.res_hor.setText(f"{r_hor:.8}"); 
    self.step_hor.setText(str(i_hor))
    self.res_kac.setText(f"{r_kac:.8}"); 
    self.step_kac.setText(str(i_kac))
    self.res_comba.setText(f"{r_com:.8}"); 
    self.step_comba.setText(str(i_com))
    self.res_iter.setText(f"{r_ite:.8}"); 
    self.step_iter.setText(str(i_ite))

    self.ax.clear()
    root_to_plot = r_dih if not np.isnan(r_dih) else a
    x_vals = np.linspace(root_to_plot - 2, root_to_plot + 2, 300)
    y_vals = np.array([f_core(x, f_idx) for x in x_vals])
    self.ax.plot(x_vals, y_vals, color='#3b82f6', linewidth=2, label='f(x)')
    self.ax.axhline(0, color='black', linewidth=1)
    self.ax.axvline(0, color='black', linewidth=1)
    if not np.isnan(r_dih):
        self.ax.plot(r_dih, 0, 'ro', label=f'Корень: {r_dih:.4f}')
    self.ax.grid(True, linestyle=':', alpha=0.7)
    self.ax.legend()
    self.canvas.draw()
# Основная функция вычислений и обновления интерфейса

def auto_params_setup(self):
    try:
        a_text = self.input_a.text().replace(',', '.')
        if not a_text or a_text == "-": 
            return MH(self, "Введите числовое значение a", self.input_a)
        a = float(a_text)
        f_idx = 1
        if self.radio1.isChecked(): f_idx = 1
        elif self.radio2.isChecked(): f_idx = 2
        elif self.radio3.isChecked(): f_idx = 3
        elif self.radio4.isChecked(): f_idx = 4
        b_auto = find_b_logic(f_idx, a)
        if np.isnan(b_auto): 
            QMessageBox.information(self, \
                "Автоподбор", "Не удалось найти b.")
        else:
            self.input_b.setText(f"{b_auto:.2f}")
            self.input_e.setText("0.001")
            run_calculation(self)
    except Exception as e:
        QMessageBox.critical(self, "Ошибка", f"Ошибка автоподбора: {e}")
# Функция для автоматического подбора параметров