from Style.Setteng_style import IW
# Импорт настроек пользовательского интерфейса

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QRadioButton, QGroupBox,
                             QTableWidget, QHeaderView as QHV, QFormLayout)
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
# Импорт компонентов библиотеки PyQt6 для работы с графическим интерфейсом

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FCanvas
from matplotlib.figure import Figure
# Импорт библиотеки для работы с графиками

from Function.Integral_operation import open_runge_window
# Импорт функции, отвечающая за открытия окна для работы с правилом Рунге

class IntegralWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Интегральные вычисления")
        self.setMinimumSize(1350, 850)
        self.setStyleSheet(IW)
        self.active_hint = None
        self.setWindowIcon(QIcon("Icon/integral.png"))
        self.init_ui()

    def init_ui(self):
        from Function.ui import run_calculation, live_validation, rex_int, \
            rex_float

        outer_layout = QVBoxLayout(self)
        content_layout = QHBoxLayout()
        left_side = QVBoxLayout()

        val_group = QGroupBox("Параметры вычислений")
        val_form = QFormLayout()
        
        self.input_a = QLineEdit("1.6")
        self.input_b = QLineEdit("2.2")
        self.input_n = QLineEdit("20")
        
        self.input_a.setValidator(rex_float)
        self.input_b.setValidator(rex_float)
        self.input_n.setValidator(rex_int)

        val_form.addRow("Нижний предел (a):", self.input_a)
        val_form.addRow("Верхний предел (b):", self.input_b)
        val_form.addRow("Число разбиений (n):", self.input_n)
        val_group.setLayout(val_form)
        left_side.addWidget(val_group)

        self.input_a.textChanged.connect(lambda: live_validation(self, 1))
        self.input_b.textChanged.connect(lambda: live_validation(self, 1))
        self.input_n.textChanged.connect(lambda: live_validation(self, 1))

        int_group = QGroupBox("Выбор подынтегральной функции")
        int_vbox = QVBoxLayout()
        icon_size = QSize(280, 55)

        self.radio1 = QRadioButton(" "); 
        self.radio1.setIconSize(icon_size); 
        self.radio1.setChecked(True)
        self.radio2 = QRadioButton(" "); 
        self.radio2.setIconSize(icon_size)
        self.radio3 = QRadioButton(" "); 
        self.radio3.setIconSize(icon_size)
        self.radio4 = QRadioButton(" "); 
        self.radio4.setIconSize(icon_size)

        self.radio1.toggled.connect(lambda: live_validation(self, 1))
        self.radio2.toggled.connect(lambda: live_validation(self, 1))
        self.radio3.toggled.connect(lambda: live_validation(self, 1))
        self.radio4.toggled.connect(lambda: live_validation(self, 1))

        self.radio1.setIcon(QIcon("./Icon/Integral1.png")) 
        self.radio2.setIcon(QIcon("./Icon/Integral2.png")) 
        self.radio3.setIcon(QIcon("./Icon/Integral3.png")) 
        self.radio4.setIcon(QIcon("./Icon/Integral4.png")) 

        int_vbox.addWidget(self.radio1)
        int_vbox.addWidget(self.radio2)
        int_vbox.addWidget(self.radio3)
        int_vbox.addWidget(self.radio4)
        int_group.setLayout(int_vbox)
        left_side.addWidget(int_group)

        self.btn_calc = QPushButton("Рассчитать результат")
        self.btn_runge = QPushButton("Оценка по Рунге")
        self.btn_exit = QPushButton("Выход");
        self.btn_calc.clicked.connect(lambda: run_calculation(self))
        self.btn_runge.clicked.connect(lambda: open_runge_window(self))
        self.btn_exit.clicked.connect(self.close)
        
        left_side.addSpacing(10)
        left_side.addWidget(self.btn_calc)
        left_side.addWidget(self.btn_runge)
        left_side.addWidget(self.btn_exit)
        left_side.addStretch()

        mid_side = QVBoxLayout()
        res_group = QGroupBox("Результаты методов")
        res_form = QFormLayout()
        self.res_left = QLineEdit(); 
        self.res_left.setReadOnly(True)
        self.res_right = QLineEdit(); 
        self.res_right.setReadOnly(True)
        self.res_aven = QLineEdit(); 
        self.res_aven.setReadOnly(True)
        self.res_trap = QLineEdit(); 
        self.res_trap.setReadOnly(True)
        self.res_simp = QLineEdit(); 
        self.res_simp.setReadOnly(True)
        self.res_nmin = QLineEdit(); 
        self.res_nmin.setReadOnly(True)
        res_form.addRow("Левые прямоуг.:", self.res_left)
        res_form.addRow("Правые прямоуг.:", self.res_right)
        res_form.addRow("Cредние прямоуг.:", self.res_aven)
        res_form.addRow("Метод трапеций:", self.res_trap)
        res_form.addRow("Метод Симпсона:", self.res_simp)
        res_form.addRow("Минимальное n:", self.res_nmin)
        res_group.setLayout(res_form)
        mid_side.addWidget(res_group)
        mid_side.addStretch()

        right_side = QVBoxLayout()
        table_container = QGroupBox("Узловые точки")
        table_layout = QVBoxLayout()
        RH = QHV.ResizeMode
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["xi", "f(xi)"])
        self.table.horizontalHeader().setSectionResizeMode(RH.Stretch)
        table_layout.addWidget(self.table)
        table_container.setLayout(table_layout)
        right_side.addWidget(table_container, 2)

        plot_container = QGroupBox("Визуализация")
        plot_layout = QVBoxLayout()
        self.figure = Figure(facecolor='#FFFFFF')
        self.canvas = FCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(True, linestyle='--', alpha=0.6)
        plot_layout.addWidget(self.canvas)
        plot_container.setLayout(plot_layout)
        right_side.addWidget(plot_container, 3)

        content_layout.addLayout(left_side, 2)
        content_layout.addLayout(mid_side, 2)
        content_layout.addLayout(right_side, 5)
        outer_layout.addLayout(content_layout)
# Класс, которая отвечает за окно с интегралами, графикам и таблицой
