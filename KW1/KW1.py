import sys
# Библиотека для работы со встроенным интерпретатором

from PyQt6.QtWidgets import QApplication
# Импорт компонента библиотеки PyQt6 для работы с графическим интерфейсом

from Class.Window.main_window import MainWindow
# Класс, которая отвечает за главное меню

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
# Проверка на то, что данный скрипт является основной
