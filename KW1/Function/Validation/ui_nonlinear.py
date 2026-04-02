from Class.Components.tooltip import ModernHint
# Класс, которая является созданным компонетом для вывода всплывающей 
# подсказки

from Function.Calculate.nonlinear_operation import run_calculation as clc_lgc
# Функция отвечающая за вычисления корня уравнения методом дихотомии

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import  QRegularExpressionValidator
# Импортирование встроенной функции в PyQt6 для работы с регулярными 
# выражения

float_re = QRegularExpression(r"^-?\d*[.,]?\d*$")
int_re = QRegularExpression(r"^\d*[.]?\d*$")
epc_re = QRegularExpression(r"^\d[.]\d+$")
rex_int = QRegularExpressionValidator(int_re)
rex_float = QRegularExpressionValidator(float_re)
rex_epc = QRegularExpressionValidator(epc_re)
# Настройка регулярных выражении

def run_calculation(self):
    if live_validation(self, 1):
        clear_hint(self)
        clc_lgc(self)
    else:
        print("Ошибка валидации, расчет не начат")
# Функция предназначена для запуска функции вычисления методов

def live_validation(self, index):
    wrng = "Аргумент логарифма должен быть больше 0 (x > -11)"
    update_button_state(self, index)
    if index == 1:
        text_a_b = "Левая граница (a) должна быть меньше правой границы (b)"
        text_a = self.input_a.text().replace(',', '.')
        text_b = self.input_b.text().replace(',', '.')
        text_e = self.input_e.text().replace(',', '.')
        try:
            if text_a and text_b:
                val_a = float(text_a) if text_a != "-" else 0
                val_b = float(text_b) if text_b != "-" else 0
                
                if self.radio4.isChecked():
                    if val_a <= -11:
                        return show_single_hint(self, self.input_a, wrng)
                    if val_b <= -11:
                        return show_single_hint(self, self.input_b, wrng)

                if text_a != "-" and text_b != "-":
                    if float(text_a) >= float(text_b):
                        return show_single_hint(self, self.input_a, text_a_b)
            else:
                return show_single_hint(self, self.input_a, "Введите число")
        
            if text_a == "": return show_single_hint(self, self.input_a, 
                                                     "Введите число")
            if text_b == "": return show_single_hint(self, self.input_b, 
                                                     "Введите число")
            if text_e == "": return show_single_hint(self, self.input_e, 
                                                     "Введите точность")

            if text_e:
                val_e = float(text_e)
                if val_e <= 0 or val_e > 1:
                    show_single_hint(self, self.input_e, 
                                     "Точность должна быть от 0 до 1")
                    return False 

            clear_hint(self)
            return True

        except ValueError:
            clear_hint(self)
            return False
    else:
        return True
# Функция предназначена для валидации данных

def show_single_hint(self, widget, text):
    if getattr(self, 'active_hint', None) is not None:
        if self.active_hint.text == text:
            return
        clear_hint(self)
    self.active_hint = ModernHint(self, text, widget)
    self.active_hint.show()
# Функция для проверки созданных всплывающих посказков

def clear_hint(self):
    hint = getattr(self, 'active_hint', None)
    if hint:
        if hasattr(hint, 'hide_and_delete'):
            hint.hide_and_delete()
        else:
            hint.deleteLater()
        self.active_hint = None
# Функция для очистки всплывающих подсказок

def update_button_state(self, index):
    if index == 1:
        a_str = self.input_a.text().strip().replace(',', '.')
        b_str = self.input_b.text().strip().replace(',', '.')
        e_str = self.input_e.text().strip().replace(',', '.')
        is_valid = bool(a_str and b_str and e_str and a_str != "-" and b_str != "-")

        if is_valid:
            try:
                a_val, b_val = float(a_str), float(b_str)
                e_val = float(e_str)
                if a_val >= b_val or e_val <= 0:
                    is_valid = False
                if self.radio4.isChecked() and (a_val <= -11 or b_val <= -11):
                    is_valid = False
            except:
                is_valid = False
        self.btn_calc.setEnabled(is_valid)
        self.btn_runge.setEnabled(True)
# Функция для обновления состояния кнопки с блокировкой по ОДЗ