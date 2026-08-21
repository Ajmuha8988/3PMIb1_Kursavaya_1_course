import numpy as np
from numba import njit
import math
# Библиотеки для работы с массивами и компиляции

from qtpy.QtWidgets import (QTableWidgetItem, QMessageBox)
# Импорт компонентов библиотеки PyQt6 для работы с графическим интерфейсом

from Class.Window.runge_window import RungeWindow
# Класс, хранящий окно с интегралами и отвечающий за выполнение вычисления
# погрешности правилом Рунге

from Class.Components.tooltip import ModernHint as MH
# Импорт класса всплывающей подсказки

@njit
def format_to_3_digits(value):
    val_digit = np.floor(value * 1000) / 1000
    return val_digit
# Функция для форматирования числа в строку

@njit(fastmath=True)
def f_core(x, func_idx):
    if func_idx == 1:
        return np.sqrt(1.5 * x + 0.6) / (1.6 + np.sqrt(0.8 * x**2 - 2))
    elif func_idx == 2:
        return np.cos((0.6 * (x**2)) + 0.4) / (1.4 + (np.sin(x + 0.7))**2)  
    elif func_idx == 3:
        return 1.0 / np.sqrt(2.0 * x**2 - 2.0)
    else:
        return np.cos(x) / (32.0 * x - 1.0)
# Функция с 4-мя интегралами

@njit(fastmath=True)
def nb_all_methods(func_idx, a, b, n):
    h = (b - a) / n
    s_left = 0.0
    s_mid_rect = 0.0
    s_mid_simp = 0.0
    s_even_simp = 0.0
    
    for i in range(n):
        x = a + i * h
        y = f_core(x, func_idx)
        s_left += y

        x_mid = a + (i + 0.5) * h
        s_mid_rect += f_core(x_mid, func_idx)
        
        if i > 0:
            if i % 2 == 1: 
                s_mid_simp += y
            else: 
                s_even_simp += y
            
    y_a = f_core(a, func_idx)
    y_b = f_core(b, func_idx)
    
    res_l = s_left * h
    res_r = (s_left - y_a + y_b) * h
    res_m = s_mid_rect * h
    res_t = ((y_a + y_b) / 2.0 + (s_left - y_a)) * h
    res_s = (h / 3.0) * (y_a + y_b + 4.0 * s_mid_simp + 2.0 * s_even_simp)
    
    return res_l, res_r, res_m, res_t, res_s
# Функция с 5-ми методами интегрирования

def nb_find_n_min_logic(f_idx, a, b):
    n = 2
    max_iter = 100000
    while n <= max_iter:
        res_l, res_r, res_m, res_t, res_s = nb_all_methods(f_idx, a, b, n)
        
        fmt_l = format_to_3_digits(res_l)
        fmt_r = format_to_3_digits(res_r)
        fmt_m = format_to_3_digits(res_m)
        fmt_t = format_to_3_digits(res_t)
        fmt_s = format_to_3_digits(res_s)
        
        if fmt_l == fmt_r == fmt_m == fmt_t == fmt_s:
            return n
        n += 2
    return -1
# Функция для нахождения минимального n

@njit(fastmath=True)
def nb_runge_engine(a, b, eps, f_idx):
    res_v1 = np.zeros(5)
    res_v2 = np.zeros(5)
    res_n = np.zeros(5)
    p_vals = np.array([1.0, 1.0, 2.0, 2.0, 4.0])
    done = np.array([False, False, False, False, False])
    
    n = 4
    while n <= 1048576:
        v1_all = nb_all_methods(f_idx, a, b, n)
        v2_all = nb_all_methods(f_idx, a, b, 2 * n)
        for i in range(5):
            if not done[i]:
                if abs(v2_all[i] - v1_all[i]) / (2**p_vals[i] - 1) <= eps:
                    res_v1[i], res_v2[i], res_n[i] = v1_all[i], v2_all[i], n
                    done[i] = True
        if done[0] and done[1] and done[2] and done[3] and done[4]: 
            break
        n *= 2
    return res_v1, res_v2, res_n
# Функция вычисления метода Рунге

@njit(fastmath=True)
def ODS_1(a):
    if (0.8 * a**2 - 2) > 0: 
        return 0
    else:
        return -1
# ОДЗ

@njit(fastmath=True)
def ODS_3(a, b):
    if -1 <= a <= 1: 
        return -1
    else:
        if -1 <= b <= 1:
            return -2
        else:
            if a <= 1 and b >= -1:
                return -3
            else:
                return 0
# ОДЗ

def val_a_and_b(self):
    MH(self, "Нижний предел (a) должен быть меньше (b)", self.input_a)
# Валидация

def val_n(self):
    MH(self, "Число разбиений n должно быть > 0", self.input_n)
# Валидация

def clear_ui(self):
    for field in [self.res_left, self.res_right, self.res_aven, 
                  self.res_trap, self.res_simp, self.res_nmin]:
        field.clear()
    self.table.setRowCount(0)
    self.ax.clear()
    self.canvas.draw()
# Функция для очищения всех значении и функции

def find_n_min(f_idx, a, b):
    res = nb_find_n_min_logic(f_idx, a, b)
    return res if res != -1 else "Не найдено"
# Функция для нахождения n минимального

def calculate(self):
    clear_ui(self)
    try:
        a = float(self.input_a.text().replace(',', '.'))
        b = float(self.input_b.text().replace(',', '.'))
        n = int(self.input_n.text())
        if a > b: 
            return val_a_and_b(self)
        if n <= 0: 
            return val_n(self)

        f_idx = 1
        if self.radio1.isChecked():
            f_idx = 1
        elif self.radio2.isChecked():
            f_idx = 2
        elif self.radio3.isChecked():
            f_idx = 3
        else:
            f_idx = 4
        
        h = (b - a) / n

        self.table.setRowCount(min(n + 1, 500))
        for i in range(min(n + 1, 500)):
            xi = a + i * h
            yi = f_core(xi, f_idx)
            self.table.setItem(i, 0, QTableWidgetItem(f"{xi:.10}"))
            self.table.setItem(i, 1, QTableWidgetItem(f"{yi:.10}"))
        
        for i in range(self.table.rowCount()):
            self.table.setVerticalHeaderItem(i, QTableWidgetItem(str(i)))

        res_l, res_r, res_m, res_t, res_s = nb_all_methods(f_idx, a, b, n)
        self.res_left.setText(f"{res_l:.10}")
        self.res_right.setText(f"{res_r:.10}")
        self.res_aven.setText(f"{res_m:.10}")
        self.res_trap.setText(f"{res_t:.10}")
        self.res_simp.setText(f"{res_s:.10}")

        self.res_nmin.setText(str(find_n_min(f_idx, a, b)))

        x_vals = np.linspace(a, b, 200)
        y_vals = np.array([f_core(x, f_idx) for x in x_vals])
        self.ax.plot(x_vals, y_vals, color='#3b82f6', linewidth=2)
        self.ax.fill_between(x_vals, y_vals, color='#3b82f6', alpha=0.1)
        self.ax.grid(True, linestyle=':', alpha=0.7)
        self.canvas.draw()
    except Exception as e:
        QMessageBox.critical(self, "Ошибка", f"Ошибка: {e}")
# Функция для полного расчёта всех методов интегрирования и число n минимальная

def open_runge_window(self):
    self.runge_dialog = RungeWindow(self)
    self.runge_dialog.exec()
# Функция для открытия окна Рунге

def calculate_runge_logic(self):
    w_text = "Число не должно превышать 1, но и не должно быть меньше 0"
    try:
        raw_eps = self.eps_input.text().replace(',', '.')
        if not raw_eps:
            return MH(self, "Введите точность", self.eps_input)
        
        eps = float(raw_eps)
        if eps < 0 or eps > 1:
            return MH(self, w_text, self.eps_input)

        a = float(self.parent.input_a.text().replace(',', '.'))
        b = float(self.parent.input_b.text().replace(',', '.'))

        f_idx = 1
        for i, rb in enumerate(self.radio_group):
            if rb.isChecked():
                f_idx = i + 1
                break

        v1, v2, ns = nb_runge_engine(a, b, eps, f_idx)
        keys = ["left", "right", "aven", "trap", "simp"]

        for i, key in enumerate(keys):
            if ns[i] > 0:
                self.res_rows[key]["n_edit"].setText(f"{v1[i]:.10f}")
                self.res_rows[key]["n2_edit"].setText(f"{v2[i]:.10f}")
                self.res_rows[key]["final_n_edit"].setText(str(int(ns[i])))
            else:
                self.res_rows[key]["n_edit"].setText(f"{v1[i]:.10f}") 
                self.res_rows[key]["n2_edit"].setText(f"{v2[i]:.10f}")
                self.res_rows[key]["final_n_edit"].setText("превышен лимит")
    except Exception as e:
        QMessageBox.critical(self, "Ошибка", f"Ошибка: {e}")
# Функция для полного вычисления точности методом Рунге