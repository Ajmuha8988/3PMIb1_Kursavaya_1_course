import numpy as np
from numba import njit
# Библиотеки для работы с массивами и быстрыми вычислениями

from PyQt6.QtWidgets import (QTableWidgetItem, QMessageBox)
# Импорт компонентов библиотеки PyQt6 для работы с графическим интерфейсом

from Class.Components.tooltip import ModernHint as MH
# Импорт класса всплывающей подсказки

@njit(fastmath=True, cache=True)
def f_core(x, func_idx):
    if func_idx == 1:
        return 3**x + 2*x - 5
    elif func_idx == 2:
        return x**4 - 4*x**3 - 8*x**2 + 1
    elif func_idx == 3:
        return x**2 - 3 + 0.5**x
    else:
        if x <= -11: return np.nan
        return ((x - 2)**2) * np.log10(x + 11) - 1
# Функция-ядро для максимально быстрого вычисления математических формул

@njit(fastmath=True)
def bisection_method(func_idx, a, b, eps):
    fa = f_core(a, func_idx)
    fb = f_core(b, func_idx)
    
    if fa == 0: return a, 0
    if fb == 0: return b, 0
    if fa * fb > 0:
        return np.nan, -1
    
    iters = 0
    while (b - a) > eps:
        c = (a + b) / 2
        fc = f_core(c, func_idx)
        if fc == 0:
            return c, iters
        if fa * fc < 0:
            b = c
        else:
            a = c
            fa = fc
        iters += 1
    
    return (a + b) / 2, iters
# Функция, реализующая алгоритм метода дихотомии

@njit(fastmath=True)
def find_b_logic(func_idx, a):
    step = 0.4
    val_a = f_core(a, func_idx)
    for i in range(1, 500):
        for direction in [1.0, -1.0]:
            b_candidate = a + i * step * direction
            val_b = f_core(b_candidate, func_idx)
            if not np.isnan(val_b):
                if val_a * val_b <= 0:
                    return b_candidate
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
    try:
        a = float(self.input_a.text().replace(',', '.'))
        b = float(self.input_b.text().replace(',', '.'))
        eps = float(self.input_e.text().replace(',', '.'))

        f_idx = 1
        if self.radio2.isChecked(): f_idx = 2
        elif self.radio3.isChecked(): f_idx = 3
        elif self.radio4.isChecked(): f_idx = 4

        if f_idx == 4 and (a <= -11 or b <= -11):
            return QMessageBox.warning(self, "Ошибка", \
                "Границы вне области определения (x > -11)")

        result, iters = bisection_method(f_idx, a, b, eps)

        if np.isnan(result):
            return val_a_and_b(self)
        
        self.res_dih.setText(f"{result:.6f}")
        self.step_dih.setText(str(iters))

        self.ax.clear()
        plot_min, plot_max = result - 2, result + 2
        x_vals = np.linspace(plot_min, plot_max, 300)
        y_vals = np.array([f_core(x, f_idx) for x in x_vals])
        
        self.ax.plot(x_vals, y_vals, color='#3b82f6', linewidth=2, \
            label='f(x)')
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)
        self.ax.plot(result, 0, 'ro', label=f'Корень: {result:.4f}')
        
        self.ax.grid(True, linestyle=':', alpha=0.7)
        self.ax.legend()
        self.canvas.draw()

    except Exception as e:
        QMessageBox.critical(self, "Ошибка", f"Ошибка: {e}")
# Основная функция вычислений и обновления интерфейса

def auto_params_setup(self):
    try:
        a_text = self.input_a.text().replace(',', '.')
        if not a_text or a_text == "-":
            return MH(self, "Введите числовое значение a", self.input_a)
        
        a = float(a_text)
        f_idx = 1
        if self.radio2.isChecked(): f_idx = 2
        elif self.radio3.isChecked(): f_idx = 3
        elif self.radio4.isChecked(): f_idx = 4
        
        b_auto = find_b_logic(f_idx, a)
        if np.isnan(b_auto):
            QMessageBox.information(self, "Автоподбор", \
                "Не удалось автоматически найти b.")
        else:
            self.input_b.setText(f"{b_auto:.2f}")
            self.input_e.setText("0.001")
            run_calculation(self)
    except Exception as e:
        QMessageBox.critical(self, "Ошибка", f"Ошибка автоподбора: {e}")
# Функция для автоматического подбора параметров