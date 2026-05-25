import numpy as np
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import QRegularExpression, Qt
from PyQt6.QtGui import QRegularExpressionValidator
# Импорт компонентов для работы с интерфейсом и валидацией

from Class.Components.tooltip import ModernHint as MH
# Импорт класса всплывающей подсказки

from Function.Calculate.poly_operation import (get_canonical_coeffs,
                                               poly_lagrange,
                                              poly_newton, 
                                              format_universal_formula)

float_re = QRegularExpression(r"^-?\d*[.,]?\d*$")
rex_float = QRegularExpressionValidator(float_re)
# Настройка регулярных выражений

def live_validation(self, index):
    update_button_state(self)
    if index == 1:
        x_text = self.input_x.text().replace(',', '.')
        y_text = self.input_y.text().replace(',', '.')
        
        if x_text == "": 
            clear_hint(self, self.input_y)
            return show_single_hint(self, self.input_x, "Введите X")
        if x_text == "-": 
            clear_hint(self, self.input_y)
            return show_single_hint(self, self.input_x, "Неполное число")
        if y_text == "": 
            clear_hint(self, self.input_x)
            return show_single_hint(self, self.input_y, "Введите Y")
        if y_text == "-": 
            clear_hint(self, self.input_x)
            return show_single_hint(self, self.input_y, "Неполное число")
        
        try:
            x_val = float(x_text)
            for i in range(self.table_points.rowCount()):
                tbl_val = float(self.table_points.item(i, 0).text())
                if abs(tbl_val - x_val) < 1e-9:
                    clear_hint(self, self.input_y)
                    return show_single_hint(self, self.input_x, "Узел с таким X уже есть")
        except ValueError:
            pass
        
        clear_hint(self, self.input_x)
        clear_hint(self, self.input_y)
    
    elif index == 2:
        e_text = self.input_interp_x.text().replace(',', '.')
        if e_text == "": 
            show_single_hint(self, self.input_interp_x, "Введите точку X")
            if self.table_points.rowCount() >= 2:
                run_interpolation(self)
            return
        if e_text == "-": 
            show_single_hint(self, self.input_interp_x, "Неполное число")
            if self.table_points.rowCount() >= 2:
                run_interpolation(self)
            return
            
        # Проверка на выход за границы интервала (экстраполяция)
        if self.table_points.rowCount() >= 2:
            try:
                x_vals = [float(self.table_points.item(i, 0).text()) for i in range(self.table_points.rowCount())]
                x_min, x_max = min(x_vals), max(x_vals)
                val = float(e_text)
                if val < x_min or val > x_max:
                    show_single_hint(self, self.input_interp_x, f"Точка вне диапазона [{x_min}, {x_max}]")
                    run_interpolation(self)
                    return
            except ValueError:
                pass
                
        clear_hint(self, self.input_interp_x)
        if self.table_points.rowCount() >= 2:
            run_interpolation(self)
# Функция предназначена для живой валидации данных

def update_button_state(self):
    x_text = self.input_x.text().strip().replace(',', '.')
    y_text = self.input_y.text().strip().replace(',', '.')
    
    can_add = bool(x_text and y_text and x_text != "-" and y_text != "-")
    if can_add:
        try:
            x_val = float(x_text)
            for i in range(self.table_points.rowCount()):
                tbl_val = float(self.table_points.item(i, 0).text())
                if abs(tbl_val - x_val) < 1e-9:
                    can_add = False
                    break
        except ValueError:
            can_add = False
            
    self.btn_add.setEnabled(can_add)
# Функция обновления состояния кнопок

def show_single_hint(self, widget, text):
    if not hasattr(self, 'active_hints'):
        self.active_hints = {}
        
    if widget in self.active_hints:
        if self.active_hints[widget].text == text: 
            return
        clear_hint(self, widget)
        
    self.active_hints[widget] = MH(self, text, widget)
    self.active_hints[widget].show()
# Функция для управления всплывающими подсказками

def clear_hint(self, widget=None):
    if not hasattr(self, 'active_hints'):
        self.active_hints = {}
        
    if widget:
        if widget in self.active_hints:
            hint = self.active_hints[widget]
            if hint:
                if hasattr(hint, 'hide_and_delete'): 
                    hint.hide_and_delete()
                else: 
                    hint.deleteLater()
            del self.active_hints[widget]
    else:
        widgets = list(self.active_hints.keys())
        for w in widgets:
            hint = self.active_hints[w]
            if hint:
                if hasattr(hint, 'hide_and_delete'): 
                    hint.hide_and_delete()
                else: 
                    hint.deleteLater()
        self.active_hints.clear()
        
        if getattr(self, 'active_hint', None) is not None:
            if hasattr(self.active_hint, 'hide_and_delete'): 
                self.active_hint.hide_and_delete()
            else: 
                self.active_hint.deleteLater()
            self.active_hint = None
# Функция для очистки подсказок

def add_point(self):
    x_str = self.input_x.text().strip().replace(',', '.')
    y_str = self.input_y.text().strip().replace(',', '.')

    if not x_str or not y_str or x_str == "-" or y_str == "-":
        return

    try:
        new_x = float(x_str)
        new_y = float(y_str)
    except ValueError:
        return

    points = []
    for i in range(self.table_points.rowCount()):
        px = float(self.table_points.item(i, 0).text())
        py = float(self.table_points.item(i, 1).text())
        if abs(px - new_x) < 1e-9:
            return
        points.append((px, py))

    points.append((new_x, new_y))
    points.sort(key=lambda p: p[0])

    self.table_points.setRowCount(0)
    for px, py in points:
        row = self.table_points.rowCount()
        self.table_points.insertRow(row)
        
        item_x = QTableWidgetItem(str(px))
        item_y = QTableWidgetItem(str(py))

        item_x.setFlags(item_x.flags() & ~Qt.ItemFlag.ItemIsEditable)
        item_y.setFlags(item_y.flags() & ~Qt.ItemFlag.ItemIsEditable)
        
        self.table_points.setItem(row, 0, item_x)
        self.table_points.setItem(row, 1, item_y)
        
    self.input_x.clear()
    self.input_y.clear()
    
    run_interpolation(self)
    update_button_state(self)
# Добавление точки

def fill_by_condition(self):
    clear_all(self)
    self.input_interp_x.setText("0.1")
    points = [(-0.2, 0.0), (0.0, -0.2), (0.2, 0.5), (0.4, 3.0),
              (0.6, 4.0), (0.8, 4.1)]
    for x, y in points:
        row = self.table_points.rowCount()
        self.table_points.insertRow(row)
        
        item_x = QTableWidgetItem(str(x))
        item_y = QTableWidgetItem(str(y))
        
        item_x.setFlags(item_x.flags() & ~Qt.ItemFlag.ItemIsEditable)
        item_y.setFlags(item_y.flags() & ~Qt.ItemFlag.ItemIsEditable)
        
        self.table_points.setItem(row, 0, item_x)
        self.table_points.setItem(row, 1, item_y)
        
    run_interpolation(self)
    update_button_state(self)
# Заполнение по условию

def delete_selected(self):
    indices = self.table_points.selectionModel().selectedRows()
    for index in sorted(indices, reverse=True):
        self.table_points.removeRow(index.row())
    
    if self.table_points.rowCount() >= 2:
        run_interpolation(self)
    else:
        self.ax.clear()
        self.canvas.draw()
        self.res_lagrange.clear()
        self.res_newton.clear()
        self.res_canonical.clear()
    update_button_state(self)
# Удаление точки

def clear_all(self):
    clear_hint(self)
    self.table_points.setRowCount(0)
    self.res_lagrange.clear()
    self.res_newton.clear()
    self.res_canonical.clear()
    self.label_formula.setText("Универсальная формула: ")
    self.ax.clear()
    self.ax.grid(True, linestyle='--', alpha=0.6)
    self.canvas.draw()
    update_button_state(self)
# Очистка всего

def run_interpolation(self):
    try:
        n = self.table_points.rowCount()
        if n < 2: return
        
        points = []
        for i in range(n):
            points.append((float(self.table_points.item(i,0).text()),
                           float(self.table_points.item(i,1).text())))
        points.sort()
        x_data = np.array([p[0] for p in points])
        y_data = np.array([p[1] for p in points])

        x_interp_text = self.input_interp_x.text().strip().replace(',', '.')

        if not x_interp_text or x_interp_text == "-":
            self.res_lagrange.setText("Вы не задали точку интерполяции")
            self.res_newton.setText("Вы не задали точку интерполяции")
            self.res_canonical.setText("Вы не задали точку интерполяции")
            self.label_formula.setText("Универсальная формула: ")
            self.ax.clear()
            self.ax.grid(True, linestyle='--', alpha=0.6)
            self.canvas.draw()
            return

        x_interp = float(x_interp_text)

        # Определение границ интервала
        x_min, x_max = x_data[0], x_data[-1]

        # Если точка выходит за пределы, вычисления не производятся
        if x_interp < x_min or x_interp > x_max:
            self.res_lagrange.setText("Вне диапазона")
            self.res_newton.setText("Вне диапазона")
            self.res_canonical.setText("Вне диапазона")
            self.label_formula.setText("Универсальная формула: ")
            
            # Показываем подсказку о выходе за диапазон у нужного поля
            show_single_hint(self, self.input_interp_x, f"Точка вне диапазона [{x_min}, {x_max}]")
            
            # Отрисовка только графика функции и узлов без точки интерполяции
            self.ax.clear()
            self.ax.plot(x_data, y_data, '-', color='#3b82f6', linewidth=2, 
                         label='P(x)')
            self.ax.scatter(x_data, y_data, color='red', zorder=3, 
                            label='Узлы')
            self.ax.legend()
            self.ax.grid(True, linestyle='--', alpha=0.6)
            self.canvas.draw()
            return
        else:
            # Если точка в диапазоне — убираем предупреждение об экстраполяции у поля x*
            clear_hint(self, self.input_interp_x)

        coeffs = get_canonical_coeffs(x_data, y_data)
        if coeffs:
            res_c = sum(c * (x_interp ** i) for i, c in enumerate(coeffs))
            self.res_canonical.setText(f"{res_c:.6f}")
            self.label_formula.setText(f"Универсальная формула: \
 {format_universal_formula(coeffs)}")
        
        self.res_lagrange.setText(f"{poly_lagrange(x_interp, x_data, 
        y_data):.6f}")
        self.res_newton.setText(f"{poly_newton(x_interp, x_data, 
        y_data):.6f}")

        self.ax.clear()
        self.ax.plot(x_data, y_data, '-', color='#3b82f6', linewidth=2, 
                     label='P(x)')
        self.ax.scatter(x_data, y_data, color='red', zorder=3, 
                        label='Узлы')
        self.ax.legend()
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.canvas.draw()
    except Exception:
        pass
# Расчет и отрисовка