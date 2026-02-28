from PyQt6.QtCore import  pyqtSlot
from PyQt6.QtWidgets import QMessageBox
# Импорт компонента библиотеки PyQt6 для работы с графическим интерфейсом

from PyQt6.QtCore import  pyqtSlot

from Class.Window.intergral_window import IntegralWindow
# Класс, которая отвечает за окно с интегралами, графикам и таблицой 

@pyqtSlot(str)
def _on_topic_click(self, topic_name):
    open_topic(self, topic_name)
# Функция посредник между анимации загрузки в кнопке и открытия нового окна

def open_topic(parent, topic_name):
    if topic_name == "Интегралы":
        if parent.integral_ui is None:
            parent.integral_ui = IntegralWindow(parent)
        
        parent.integral_ui.show()
        parent.integral_ui.raise_()
        parent.integral_ui.activateWindow()

    elif topic_name == "Нелинейные уравнения":
        QMessageBox.information(parent, "В разработке", f"Раздел \
        '{topic_name}' скоро появится!")
    else:
        print(f"Логика для '{topic_name}' не описана в navigation.py")
# Функция предназначена для навигации окон