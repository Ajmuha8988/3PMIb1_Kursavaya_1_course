import numpy as np
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import QRegularExpression, Qt
from PyQt6.QtGui import QRegularExpressionValidator
# Импорт компонентов для работы с интерфейсом и валидацией

from Class.Components.tooltip import ModernHint as MH
# Импорт класса всплывающей подсказки

from Function.Calculate.diff_operation import solve_bvp
# Импорт метода численного решения краевой задачи МКР

from Function.Calculate.poly_operation import (get_canonical_coeffs,
                                              format_universal_formula,
                                              poly_lagrange)
# Импорт канонического полинома из файла poly_operation

float_re = QRegularExpression(r"^-?\d*[.,]?\d*$")
rex_float = QRegularExpressionValidator(float_re)
# Настройка регулярных выражений

def live_validation(self, index):
    update_button_state(self)
    if index == 1:
        x_start_txt = self.input_x_start.text().replace(',', '.')
        x_end_txt = self.input_x_end.text().replace(',', '.')
        n_txt = self.input_n.text().strip()
        
        if x_start_txt == "":
            clear_hint(self, self.input_x_end)
            return show_single_hint(self, self.input_x_start, 
                                    "Введите x нач")
        if x_end_txt == "":
            clear_hint(self, self.input_x_start)
            return show_single_hint(self, self.input_x_end, "Введите x кон")
            
        try:
            xs = float(x_start_txt)
            xe = float(x_end_txt)
            if xs >= xe:
                return show_single_hint(self, self.input_x_end, 
                                        "x нач должно быть < x кон")
            if int(n_txt) < 1:
                return show_single_hint(self, self.input_n, 
                                        "Количество отрезков должно \
 быть больше 0")
        except ValueError:
            pass
            
        clear_hint(self, self.input_x_start)
        clear_hint(self, self.input_x_end)
        
    elif index == 2:
        n_txt = self.input_n.text().strip()
        if n_txt == "":
            return show_single_hint(self, self.input_n, "Введите n")
        if int(n_txt) < 1:
            return show_single_hint(self, self.input_n, 
                                        "Количество отрезков должно \
 быть больше 0")
        clear_hint(self, self.input_n)
# Функция предназначена для живой валидации данных

def update_button_state(self):
    p_txt = self.input_px.text().strip()
    q_txt = self.input_qx.text().strip()
    f_txt = self.input_fx.text().strip()
    xs_txt = self.input_x_start.text().strip().replace(',', '.')
    xe_txt = self.input_x_end.text().strip().replace(',', '.')
    ys_txt = self.input_y_start.text().strip().replace(',', '.')
    ye_txt = self.input_y_end.text().strip().replace(',', '.')
    n_txt = self.input_n.text().strip()
    
    can_calc = bool(p_txt and q_txt and f_txt and xs_txt and xe_txt 
                    and ys_txt and ye_txt and n_txt)
    if can_calc:
        try:
            xs = float(xs_txt)
            xe = float(xe_txt)
            n = int(n_txt)
            if xs >= xe or n <= 0:
                can_calc = False
        except ValueError:
            can_calc = False
            
    self.btn_calc.setEnabled(can_calc)
# Функция обновления состояния кнопок

def show_single_hint(self, widget, text):
    if not hasattr(self, 'active_hints'):
        self.active_hints = {}
        
    if widget in self.active_hints:
        hint = self.active_hints[widget]
        try:
            if hint and hint.text == text: 
                return
        except RuntimeError:
            pass
        clear_hint(self, widget)
        
    try:
        self.active_hints[widget] = MH(self, text, widget)
        self.active_hints[widget].show()
    except Exception:
        pass
# Функция для управления всплывающими подсказками

def clear_hint(self, widget=None):
    if not hasattr(self, 'active_hints'):
        self.active_hints = {}
        
    if widget:
        if widget in self.active_hints:
            hint = self.active_hints[widget]
            if hint:
                try:
                    if hasattr(hint, 'hide_and_delete'): 
                        hint.hide_and_delete()
                    else: 
                        hint.deleteLater()
                except RuntimeError:
                    pass
            del self.active_hints[widget]
    else:
        widgets = list(self.active_hints.keys())
        for w in widgets:
            hint = self.active_hints[w]
            if hint:
                try:
                    if hasattr(hint, 'hide_and_delete'): 
                        hint.hide_and_delete()
                    else: 
                        hint.deleteLater()
                except RuntimeError:
                    pass
        self.active_hints.clear()
        
        if getattr(self, 'active_hint', None) is not None:
            try:
                if hasattr(self.active_hint, 'hide_and_delete'): 
                    self.active_hint.hide_and_delete()
                else: 
                    self.active_hint.deleteLater()
            except RuntimeError:
                pass
            self.active_hint = None
# Функция для очистки подсказок

def fill_by_condition(self):
    clear_all(self)
    self.input_px.setText("-x")
    self.input_qx.setText("-2")
    self.input_fx.setText("x*cos(x)")
    self.input_x_start.setText("0.5")
    self.input_y_start.setText("0.479")
    self.input_x_end.setText("1.5")
    self.input_y_end.setText("0.997")
    self.input_n.setText("9")
    update_button_state(self)
# Заполнение по условию

def clear_all(self):
    clear_hint(self)
    self.input_px.clear()
    self.input_qx.clear()
    self.input_fx.clear()
    self.input_x_start.clear()
    self.input_y_start.clear()
    self.input_x_end.clear()
    self.input_y_end.clear()
    self.input_n.clear()
    self.res_polynomial.clear()
    self.table_results.setRowCount(0)
    self.ax.clear()
    self.ax.grid(True, linestyle='--', alpha=0.6)
    self.canvas.draw()
    update_button_state(self)
# Очистка всего

def run_calculation(self):
    p_str = self.input_px.text().strip()
    q_str = self.input_qx.text().strip()
    f_str = self.input_fx.text().strip()
    
    try:
        x_start = float(self.input_x_start.text().replace(',', '.'))
        y_start = float(self.input_y_start.text().replace(',', '.'))
        x_end = float(self.input_x_end.text().replace(',', '.'))
        y_end = float(self.input_y_end.text().replace(',', '.'))
        n = int(self.input_n.text())
    except ValueError:
        return

    if x_start >= x_end:
        show_single_hint(self, self.input_x_end, 
                         "x_нач должен быть меньше x_кон")
        return

    if n <= 0:
        show_single_hint(self, self.input_n, 
                         "n не может быть меньше или равен 0")
        return

    if n == 1:
        self.ax.clear()
        x = np.array([x_start, x_end])
        y = np.array([y_start, y_end])
        coeffs = get_canonical_coeffs(x, y)
        self.res_polynomial.setText(f"Универсальная формула: \
 {format_universal_formula(coeffs)}")
        xi_line = np.linspace(x_start, x_end, 200)
        y_lagrange = [poly_lagrange(xi, x, y) for xi in xi_line]
        self.ax.plot(xi_line, y_lagrange, '-', color='#3b82f6', linewidth=2, 
                         label='Полином')
        for xi, yi in zip(x, y):
            row = self.table_results.rowCount()
            self.table_results.insertRow(row)
            
            item_x = QTableWidgetItem(f"{xi:.6f}")
            item_y = QTableWidgetItem(f"{yi:.6f}")
            item_x.setFlags(item_x.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item_y.setFlags(item_y.flags() & ~Qt.ItemFlag.ItemIsEditable)
            
            self.table_results.setItem(row, 0, item_x)
            self.table_results.setItem(row, 1, item_y)

        self.ax.scatter(x, y, color='red', zorder=3, label='Узлы')
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.legend()
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.canvas.draw()
        return

    if self.radio_thomas.isChecked():
        method = 'thomas'
    elif self.radio_matrix.isChecked():
        method = 'matrix'
    elif self.radio_gauss.isChecked():
        method = 'gauss'
    elif self.radio_cramer.isChecked():
        method = 'cramer'
        if n - 1 > 5:
            show_single_hint(self, self.input_n, 
                             "Для Крамера n должно быть <= 6")
            return
    else:
        method = 'thomas'

    try:
        x_sol, y_sol = solve_bvp(p_str, q_str, f_str, x_start, y_start, 
                                 x_end, y_end, n, method)
        coeffs = get_canonical_coeffs(x_sol, y_sol)
        
        self.table_results.setRowCount(0)
        for xi, yi in zip(x_sol, y_sol):
            row = self.table_results.rowCount()
            self.table_results.insertRow(row)
            
            item_x = QTableWidgetItem(f"{xi:.6f}")
            item_y = QTableWidgetItem(f"{yi:.6f}")
            item_x.setFlags(item_x.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item_y.setFlags(item_y.flags() & ~Qt.ItemFlag.ItemIsEditable)
            
            self.table_results.setItem(row, 0, item_x)
            self.table_results.setItem(row, 1, item_y)
        
        self.ax.clear()

        if coeffs:
            self.res_polynomial.setText(format_universal_formula(coeffs))
            x_plot = np.linspace(x_start, x_end, 200)
            y_poly = sum(c * (x_plot ** i) for i, c in enumerate(coeffs))
            self.ax.plot(x_plot, y_poly, '-', color='#3b82f6', linewidth=2, 
                         label='Полином')
        else:
            self.res_polynomial.setText("Не удалось рассчитать полином")
            self.ax.plot(x_sol, y_sol, '-', color='#3b82f6', linewidth=2, 
                         label='Полином')

        self.ax.scatter(x_sol, y_sol, color='red', zorder=3, label='Узлы')
        
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.legend()
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.canvas.draw()

    except Exception as e:
        show_single_hint(self, self.btn_calc, f"Ошибка расчетов: {str(e)}")
# Расчет и отрисовка