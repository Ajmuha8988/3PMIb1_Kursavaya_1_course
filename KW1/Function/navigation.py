from PyQt6.QtWidgets import QMessageBox
# Импорт компонента библиотеки PyQt6 для работы с графическим интерфейсом

import os
import webbrowser
from Class.Window.intergral_window import IntegralWindow
from Class.Window.nonlinear_window import NonlinearWindow
from Class.Window.poly_window import PolyWindow
from Class.Window.approx_window import ApproxWindow
from Class.Window.diff_window import DiffWindow
# Класс, которая отвечает за окно с интегралами, графикам и таблицой 

topics = [
            "Интегралы",
            "Нелинейные уравнения",
            "Аппроксимация",
            "Интерполяция",
            "Дифференциальные уравнения",
            "От автора"
        ]
# Массив с названием разделом

def open_topic(parent, topic_name):
    if topic_name == "Интегралы":
        if parent.integral_ui is None:
            parent.integral_ui = IntegralWindow(parent)
        
        parent.integral_ui.show()
        parent.integral_ui.raise_()
        parent.integral_ui.activateWindow()

    if topic_name == "Нелинейные уравнения":
        if parent.nonlinear_ui is None:
            parent.nonlinear_ui = NonlinearWindow(parent)
        
        parent.nonlinear_ui.show()
        parent.nonlinear_ui.raise_()
        parent.nonlinear_ui.activateWindow()
    elif topic_name == "Интерполяция":
        if parent.poly_ui is None:
            parent.poly_ui = PolyWindow(parent)
        
        parent.poly_ui.show()
        parent.poly_ui.raise_()
        parent.poly_ui.activateWindow()
    elif topic_name == "Аппроксимация":
        if parent.approx_ui is None:
            parent.approx_ui = ApproxWindow(parent)
        
        parent.approx_ui.show()
        parent.approx_ui.raise_()
        parent.approx_ui.activateWindow()
    elif topic_name == "Дифференциальные уравнения":
        if parent.diff_ui is None:
            parent.diff_ui = DiffWindow(parent)
        
        parent.diff_ui.show()
        parent.diff_ui.raise_()
        parent.diff_ui.activateWindow()
    elif topic_name == "От автора":
        RdFile = webbrowser.open(r'C:\Users\Муха\Desktop\Borlakov_M.K_KW1\KW1\KW1\Function\From_author.html')
    else:
        print(f"Что-то пошло не так")
# Функция предназначена для навигации окон