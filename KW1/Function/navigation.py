from PyQt6.QtWidgets import QMessageBox
# Импорт компонента библиотеки PyQt6 для работы с графическим интерфейсом

from PyQt6.QtCore import  pyqtSlot

from Class.Window.intergral_window import IntegralWindow
from Class.Window.nonlinear_window import NonlinearWindow
# Класс, которая отвечает за окно с интегралами, графикам и таблицой 

topics = [
            "Интегралы",
            "Нелинейные уравнения",
            "Аппроксимация",
            "Интерполяция",
            "Дифференциальные уравнения"
        ]
# Массив с названием разделом

def open_topic(parent, topic_name):
    if topic_name == "Интегралы":
        if parent.integral_ui is None:
            parent.integral_ui = IntegralWindow(parent)
        
        parent.integral_ui.show()
        parent.integral_ui.raise_()
        parent.integral_ui.activateWindow()

    elif topic_name == "Нелинейные уравнения":
        if parent.nonlinear_ui is None:
            parent.nonlinear_ui = NonlinearWindow(parent)
        
        parent.nonlinear_ui.show()
        parent.nonlinear_ui.raise_()
        parent.nonlinear_ui.activateWindow()
    else:
        print(f"Логика для '{topic_name}' не описана в navigation.py")
# Функция предназначена для навигации окон