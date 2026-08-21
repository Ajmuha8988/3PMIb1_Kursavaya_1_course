import numpy as np
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import QRegularExpression, Qt
from PyQt6.QtGui import QRegularExpressionValidator
# Импорт компонентов для работы с интерфейсом и валидацией

from Class.Components.tooltip import ModernHint as MH
# Импорт класса всплывающей подсказки

from Function.Calculate.approx_operation import (fit_linear,
                              fit_quadratic,
                              fit_custom)

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
            
        # ПРОВЕРКА НА НОЛЬ: выводим подсказку, если введен 0
        try:
            x_val = float(x_text)
            if abs(x_val) < 1e-12:
                clear_hint(self, self.input_y)
                return show_single_hint(self, self.input_x, 
                                        "X не может быть равен 0")
        except ValueError:
            pass

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
                    return show_single_hint(self, self.input_x, 
                                            "Узел с таким X уже есть")
        except ValueError:
            pass
        
        clear_hint(self, self.input_x)
        clear_hint(self, self.input_y)
# Функция предназначена для живой валидации данных

def update_button_state(self):
    x_text = self.input_x.text().strip().replace(',', '.')
    y_text = self.input_y.text().strip().replace(',', '.')
    
    can_add = bool(x_text and y_text and x_text != "-" and y_text != "-")
    if can_add:
        try:
            x_val = float(x_text)
            
            if abs(x_val) < 1e-12:
                can_add = False
            else:
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

def add_point(self):
    x_str = self.input_x.text().strip().replace(',', '.')
    y_str = self.input_y.text().strip().replace(',', '.')

    if not x_str or not y_str or x_str == "-" or y_str == "-":
        return

    try:
        new_x = float(x_str)
        new_y = float(y_str)
        
        if abs(new_x) < 1e-12:
            return
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
    
    run_approximation(self)
    update_button_state(self)
# Добавление точки

def fill_by_condition(self):
    clear_all(self)
    points = [(5.07, 7.0), (5.09, 4.5), (5.11, 3.0), 
              (5.22, 2.5), (5.33, 2.3), (5.44, 1.5), 
              (5.55, 1.7), (5.62, 2.1), (5.77, 2.21),
             (5.88, 3.0), (5.99, 4.5), (6.0, 5.0)]
    for x, y in points:
        row = self.table_points.rowCount()
        self.table_points.insertRow(row)
        
        item_x = QTableWidgetItem(str(x))
        item_y = QTableWidgetItem(str(y))
        
        item_x.setFlags(item_x.flags() & ~Qt.ItemFlag.ItemIsEditable)
        item_y.setFlags(item_y.flags() & ~Qt.ItemFlag.ItemIsEditable)
        
        self.table_points.setItem(row, 0, item_x)
        self.table_points.setItem(row, 1, item_y)
        
    run_approximation(self)
    update_button_state(self)
    live_validation(self, 1)
# Заполнение по условию

def delete_selected(self):
    indices = self.table_points.selectionModel().selectedRows()
    for index in sorted(indices, reverse=True):
        self.table_points.removeRow(index.row())
    
    if self.table_points.rowCount() >= 3:
        run_approximation(self)
    else:
        self.ax.clear()
        self.canvas.draw()
        self.res_lin_a.clear()
        self.res_lin_b.clear()
        self.res_lin_sse.clear()
        self.res_quad_a.clear()
        self.res_quad_b.clear()
        self.res_quad_c.clear()
        self.res_quad_sse.clear()
        self.res_cust_a.clear()
        self.res_cust_b.clear()
        self.res_cust_c.clear()
        self.res_cust_sse.clear()
    update_button_state(self)
# Удаление точки

def clear_all(self):
    clear_hint(self)
    self.table_points.setRowCount(0)
    self.res_lin_a.clear()
    self.res_lin_b.clear()
    self.res_lin_sse.clear()
    self.res_quad_a.clear()
    self.res_quad_b.clear()
    self.res_quad_c.clear()
    self.res_quad_sse.clear()
    self.res_cust_a.clear()
    self.res_cust_b.clear()
    self.res_cust_c.clear()
    self.res_cust_sse.clear()
    self.ax.clear()
    self.ax.grid(True, linestyle='--', alpha=0.6)
    self.canvas.draw()
    update_button_state(self)
    live_validation(self, 1)
# Очистка всего

def delete_selected(self):
    indices = self.table_points.selectionModel().selectedRows()
    for index in sorted(indices, reverse=True):
        self.table_points.removeRow(index.row())

    if self.table_points.rowCount() > 0:
        run_approximation(self)
    else:
        clear_all(self)
    update_button_state(self)


def run_approximation(self):
    try:
        n = self.table_points.rowCount()

        if n < 3:
            self.res_lin_a.setText("Нужно >= 2 точек")
            self.res_lin_b.setText("Нужно >= 2 точек")
            self.res_lin_sse.setText("Нужно >= 2 точек")

            self.res_quad_a.setText("Нужно >= 3 точек")
            self.res_quad_b.setText("Нужно >= 3 точек")
            self.res_quad_c.setText("Нужно >= 3 точек")
            self.res_quad_sse.setText("Нужно >= 3 точек")

            self.res_cust_a.setText("Нужно >= 3 точек")
            self.res_cust_b.setText("Нужно >= 3 точек")
            self.res_cust_c.setText("Нужно >= 3 точек")
            self.res_cust_sse.setText("Нужно >= 3 точек")
            
            self.ax.clear()
            self.ax.grid(True, linestyle='--', alpha=0.6)
            self.canvas.draw()
            return

        points = []
        for i in range(n):
            points.append((float(self.table_points.item(i, 0).text()),
                           float(self.table_points.item(i, 1).text())))
        points.sort()
        x_data = np.array([p[0] for p in points])
        y_data = np.array([p[1] for p in points])

        self.ax.clear()
        self.ax.scatter(x_data, y_data, color='red', zorder=5, 
                        label='Экспериментальные точки')

        x_plot = np.linspace(min(x_data), max(x_data), 200)

        try:
            la, lb, lsse = fit_linear(x_data, y_data)
            self.res_lin_a.setText(f"{la:.6f}")
            self.res_lin_b.setText(f"{lb:.6f}")
            self.res_lin_sse.setText(f"{lsse:.6f}")
            y_lin = la * x_plot + lb
            self.ax.plot(x_plot, y_lin, '-', label='Линейная регрессия', 
                         linewidth=1.5)
        except Exception as e:
            self.res_lin_a.setText("Ошибка")
            self.res_lin_b.setText("Ошибка")
            self.res_lin_sse.setText(str(e))

        if n < 3:
            self.res_quad_a.setText("Нужно >= 3 точек")
            self.res_quad_b.setText("Нужно >= 3 точек")
            self.res_quad_c.setText("Нужно >= 3 точек")
            self.res_quad_sse.setText("Нужно >= 3 точек")
        else:
            try:
                qa, qb, qc, qsse = fit_quadratic(x_data, y_data)
                self.res_quad_a.setText(f"{qa:.6f}")
                self.res_quad_b.setText(f"{qb:.6f}")
                self.res_quad_c.setText(f"{qc:.6f}")
                self.res_quad_sse.setText(f"{qsse:.6f}")
                y_quad = qa * (x_plot**2) + qb * x_plot + qc
                self.ax.plot(x_plot, y_quad, '--', 
                             label='Квадратичная регрессия', linewidth=1.5)
            except Exception as e:
                self.res_quad_a.setText("Ошибка")
                self.res_quad_b.setText("Ошибка")
                self.res_quad_c.setText("Ошибка")
                self.res_quad_sse.setText(str(e))

        if n < 3:
            self.res_cust_a.setText("Нужно >= 3 точек")
            self.res_cust_b.setText("Нужно >= 3 точек")
            self.res_cust_c.setText("Нужно >= 3 точек")
            self.res_cust_sse.setText("Нужно >= 3 точек")
        else:
            has_zero = any(abs(xi) < 1e-12 for xi in x_data)
            if has_zero:
                self.res_cust_a.setText("x = 0 присутствует")
                self.res_cust_b.setText("x = 0 присутствует")
                self.res_cust_c.setText("x = 0 присутствует")
                self.res_cust_sse.setText("x = 0 присутствует")
            else:
                try:
                    ca, cb, cc, csse = fit_custom(x_data, y_data)
                    self.res_cust_a.setText(f"{ca:.6f}")
                    self.res_cust_b.setText(f"{cb:.6f}")
                    self.res_cust_c.setText(f"{cc:.6f}")
                    self.res_cust_sse.setText(f"{csse:.6f}")
                    y_cust = ca / (x_plot**2) + cb / x_plot + cc
                    self.ax.plot(x_plot, y_cust, ':', 
                                 label='Пользовательская регрессия', 
                                 linewidth=1.5)
                except Exception as e:
                    self.res_cust_a.setText("Ошибка")
                    self.res_cust_b.setText("Ошибка")
                    self.res_cust_c.setText("Ошибка")
                    self.res_cust_sse.setText(str(e))

        self.ax.legend()
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.canvas.draw()
    except Exception:
        pass
# Расчет и отрисовка