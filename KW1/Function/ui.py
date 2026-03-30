from Class.Components.tooltip import ModernHint
# Класс, которая является созданным компонетом для вывода всплывающей 
# подсказки

from Function.Integral_operation import calculate, ODS_1, ODS_3
# Функция отвечающая за вычисления определенного интеграла всеми способами

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import  QRegularExpressionValidator
# Импортирование встроенной функции в PyQt6 для работы с регулярными 
# выражения

float_re = QRegularExpression(r"^-?\d*[.,]?\d*$")
int_re = QRegularExpression(r"^\d*$")
epc_re = QRegularExpression(r"^\d[.]\d+$")
rex_int = QRegularExpressionValidator(int_re)
rex_float = QRegularExpressionValidator(float_re)
rex_epc = QRegularExpressionValidator(epc_re)
# Настройка регулярных выражении

def run_calculation(self):
    if live_validation(self, 1):
        clear_hint(self)
        calculate(self)
    else:
        print("Ошибка валидации, расчет не начат")
# Функция предназначена для запуска функции вычисления методов

def live_validation(self, index):
    wrng = "Число не должен равняться от -1 до 1"
    i_wrng = "Интервал не должен пересекать отрезок [-1, 1]"
    plus_text = "Введите положительное число"
    update_button_state(self, index)
    if index == 1:
        text_a_b = "Нижний предел (a) должен быть меньше (b)"
        text_a = self.input_a.text().replace(',', '.')
        text_b = self.input_b.text().replace(',', '.')
        text_n = self.input_n.text()
        try:
            if text_a and text_b:
                if self.radio1.isChecked():
                    if "-" in text_a:
                        return show_single_hint(self, self.input_a, \
                            plus_text) 
                    if "-" in text_b:
                        return show_single_hint(self, self.input_a, \
                            plus_text) 
                    else:
                        val_a = float(text_a)
                        val_b = float(text_b)
                        if val_a > val_b:
                           return show_single_hint(self, self.input_a, 
                                                text_a_b)
                        if ODS_1(val_a) == -1:
                            return show_single_hint(self, self.input_a, 
                                                "Возьмите большее число")
                elif self.radio3.isChecked():
                    val_a = float(text_a)
                    val_b = float(text_b)
                    if ODS_3(val_a, val_b) == -1 :
                        return show_single_hint(self, self.input_a, wrng)
                    if ODS_3(val_a, val_b) == -2: 
                        return show_single_hint(self, self.input_b, wrng)
                    if ODS_3(val_a, val_b) == -3: 
                        return show_single_hint(self, self.input_b, i_wrng)
                else:
                    if text_a != "-": 
                        if text_b != "-":
                            val_a = float(text_a)
                            val_b = float(text_b)
                            if val_a >= val_b:
                               return show_single_hint(self, self.input_a, 
                                                       text_a_b)
                        else:
                            return show_single_hint(self, self.input_a, 
                                                    "Введите число")
            else:
                return show_single_hint(self, self.input_a, "Введите число")
        
            if text_a == "": return show_single_hint(self, self.input_a, 
                                                     "Введите число")
            if text_b == "": return show_single_hint(self, self.input_b, 
                                                     "Введите число")
            if text_n == "": return show_single_hint(self, self.input_n, 
                                                     "Введите число")

            if text_n:
                val_n = int(text_n)
                if val_n <= 0:
                    show_single_hint(self, self.input_n, 
                                     "n должно быть больше 0")
                    return False 

            clear_hint(self)
            return True

        except ValueError:
            clear_hint(self)
            return False
    else:
        text_epc = self.eps_input.text().strip()
        try:
            text_a = self.parent.input_a.text().replace(',', '.')
            text_b = self.parent.input_b.text().replace(',', '.')
            a_val, b_val = float(text_a), float(text_b)
            if self.radio_group[0].isChecked():
                if a_val < 0 or ODS_1(a_val) != 0:
                    return show_single_hint(self, self.radio_group[0], \
                                                 plus_text)
            if self.radio_group[2].isChecked():
                if ODS_3(a_val, b_val) == -1 :
                    return show_single_hint(self, self.radio_group[2], wrng)
                if ODS_3(a_val, b_val) == -2: 
                    return show_single_hint(self, self.radio_group[2], wrng)
                if ODS_3(a_val, b_val) == -3: 
                    return show_single_hint(self, self.radio_group[2], \
                        i_wrng)

            if text_epc:
                val_epc = float(text_epc)
                w_ep = "Число должно быть больше 0 и не превышать 1"
                if val_epc > 1 or val_epc <= 0:
                    return show_single_hint(self, self.eps_input, w_ep)
            if not text_epc:
                i_ep = "Точность должна быть больше 0 и не больше 1"
                return show_single_hint(self, self.eps_input, i_ep)
            
            clear_hint(self)
            return True
        except ValueError:
            clear_hint(self)
            return False
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
        n_str = self.input_n.text().strip()
        is_valid = bool(a_str and b_str and n_str and a_str != "-" and b_str != "-")

        if is_valid:
            try:
                a_val, b_val = float(a_str), float(b_str)
                n_val = int(n_str)
                if a_val > b_val or n_val <= 0:
                    is_valid = False
                else:
                    if self.radio1.isChecked():
                        if a_val < 0 or ODS_1(a_val) != 0: 
                            is_valid = False
                    elif self.radio3.isChecked():
                        if ODS_3(a_val, b_val) != 0:
                            is_valid = False
            except:
                is_valid = False
        self.btn_calc.setEnabled(is_valid)
        self.btn_runge.setEnabled(is_valid)

    else:
        try:
            a_str = self.parent.input_a.text().strip().replace(',', '.')
            b_str = self.parent.input_b.text().strip().replace(',', '.')
            a_val, b_val = float(a_str), float(b_str)

            e_str = self.eps_input.text().strip()
            val_epc = float(e_str)

            is_valid_runge = (0 < val_epc <= 1)

            if is_valid_runge:
                if self.radio_group[0].isChecked():
                    if a_val < 0 or ODS_1(a_val) != 0:
                        is_valid_runge = False

                elif self.radio_group[2].isChecked():
                    if ODS_3(a_val, b_val) != 0:
                        is_valid_runge = False
                        
            self.btn_find.setEnabled(is_valid_runge)

        except (ValueError, AttributeError, IndexError):
            self.btn_find.setEnabled(False)    
# Функция для обновления состояния кнопки с блокировкой по ОДЗ