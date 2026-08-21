from Style import Setteng_style
# Импорт настроек пользовательского интерфейса

from PyQt6.QtCore import  pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QColor
# Импорт компонентов библиотеки PyQt6 для работы с графическим интерфейсом

from pyqt_loading_button import LoadingButton, AnimationType
# Импорт пользовательского компонента PyQt6, отвечающего за кнопку загрузки

from Function.navigation import open_topic, topics
# Импорт функции, отвечающая за навигацию окон

class MainWindow(QMainWindow):
    topic_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Инженерные вычисления")
        self.setGeometry(300, 300, 600, 550)
        self.setWindowIcon(QIcon("Icon/KW_Icon.png"))

        self.integral_ui = None
        self.nonlinear_ui = None
        self.poly_ui = None
        self.approx_ui = None
        self.diff_ui = None

        self.label = QLabel("Выберите область вычислений:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.button_container = QWidget()
        self.buttons_layout = QVBoxLayout()
        self.button_container.setLayout(self.buttons_layout)

        self.setStyleSheet(Setteng_style.IW)

        self.topic_signal.connect(lambda t: open_topic(self, t))

        for topic in topics:
            btn = LoadingButton(self)
            btn.setText(topic)
            btn.setAnimationType(AnimationType.Circle)
            btn.setAnimationColor(QColor(255, 255, 255))
            btn.setStyleSheet(Setteng_style.IW)
            btn.setAction(lambda t=topic: self.topic_signal.emit(t))
            self.buttons_layout.addWidget(btn)
            
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.button_container) 
        main_layout.setContentsMargins(30, 30, 30, 30) 

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
# Класс, которая отвечает за главное меню