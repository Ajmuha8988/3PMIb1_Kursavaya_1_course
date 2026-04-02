from Style.Setteng_style import IW
# Импорт настроек пользовательского интерфейса

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QRadioButton, QGroupBox,
                             QTableWidget, QHeaderView as QHV, QFormLayout, 
                             QGridLayout, QLabel)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
# Импорт компонентов библиотеки PyQt6 для работы с графическим интерфейсом

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FCanvas
from matplotlib.figure import Figure
# Импорт библиотеки для работы с графиками

from Function.Calculate.nonlinear_operation import auto_params_setup
# Импорт функции, отвечающая за открытия окна для работы с правилом Рунге

class NonlinearWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Нелинейные уравнения")
        self.setMinimumSize(1350, 850)
        self.setStyleSheet(IW)
        self.active_hint = None
        self.setWindowIcon(QIcon("Icon/Nonlinear/nonlinear_icon.png"))
        self.init_ui()

    def init_ui(self):
        from Function.Validation.ui_nonlinear import run_calculation, \
            live_validation, rex_int, rex_float

        outer_layout = QVBoxLayout(self)
        content_layout = QHBoxLayout()
        left_side = QVBoxLayout()

        val_group = QGroupBox("Параметры вычислений")
        val_form = QFormLayout()
        
        self.input_a = QLineEdit("0")
        self.input_b = QLineEdit("1")
        self.input_e = QLineEdit("0.001")
        
        self.input_a.setValidator(rex_float)
        self.input_b.setValidator(rex_float)
        self.input_e.setValidator(rex_int)

        val_form.addRow("Левая граница (a):", self.input_a)
        val_form.addRow("Правая граница (b):", self.input_b)
        val_form.addRow("Точность (e):", self.input_e)
        val_group.setLayout(val_form)
        left_side.addWidget(val_group)

        self.input_a.textChanged.connect(lambda: live_validation(self, 1))
        self.input_b.textChanged.connect(lambda: live_validation(self, 1))
        self.input_e.textChanged.connect(lambda: live_validation(self, 1))

        int_group = QGroupBox("Выбор нелинейного уравнения")
        int_vbox = QVBoxLayout()
        icon_size = QSize(280, 55)

        self.radio1 = QRadioButton(""); 
        self.radio1.setIconSize(icon_size); 
        self.radio1.setChecked(True)
        self.radio2 = QRadioButton(""); 
        self.radio2.setIconSize(icon_size)
        self.radio3 = QRadioButton(""); 
        self.radio3.setIconSize(icon_size)
        self.radio4 = QRadioButton(""); 
        self.radio4.setIconSize(icon_size)

        self.radio1.toggled.connect(lambda: live_validation(self, 1))
        self.radio2.toggled.connect(lambda: live_validation(self, 1))
        self.radio3.toggled.connect(lambda: live_validation(self, 1))
        self.radio4.toggled.connect(lambda: live_validation(self, 1))

        self.radio1.setIcon(QIcon("./Icon/Nonlinear/Nonlinear_1.png")) 
        self.radio2.setIcon(QIcon("./Icon/Nonlinear/Nonlinear_2.png")) 
        self.radio3.setIcon(QIcon("./Icon/Nonlinear/Nonlinear_3.png")) 
        self.radio4.setIcon(QIcon("./Icon/Nonlinear/Nonlinear_4.png")) 

        int_vbox.addWidget(self.radio1)
        int_vbox.addWidget(self.radio2)
        int_vbox.addWidget(self.radio3)
        int_vbox.addWidget(self.radio4)
        int_group.setLayout(int_vbox)
        left_side.addWidget(int_group)

        self.btn_calc = QPushButton("Рассчитать результат")
        self.btn_runge = QPushButton("Автоподбор")
        self.btn_exit = QPushButton("Выход");
        self.btn_calc.clicked.connect(lambda: run_calculation(self))
        self.btn_runge.clicked.connect(lambda: auto_params_setup(self))
        self.btn_exit.clicked.connect(self.close)
        
        left_side.addSpacing(10)
        left_side.addWidget(self.btn_calc)
        left_side.addWidget(self.btn_runge)
        left_side.addWidget(self.btn_exit)
        left_side.addStretch()

        mid_side = QVBoxLayout()
        res_group = QGroupBox("Результаты методов")
        res_grid = QGridLayout()
        res_grid.setSpacing(10)
        res_grid.setContentsMargins(15, 20, 15, 15)
        
        self.res_dih = QLineEdit(); self.res_dih.setReadOnly(True)
        self.res_hor = QLineEdit(); self.res_hor.setReadOnly(True)
        self.res_kac = QLineEdit(); self.res_kac.setReadOnly(True)
        self.res_comba = QLineEdit(); self.res_comba.setReadOnly(True)
        self.res_iter = QLineEdit(); self.res_iter.setReadOnly(True)
       
        self.step_dih = QLineEdit(); self.step_dih.setReadOnly(True); self.step_dih.setFixedWidth(80)
        self.step_hor = QLineEdit(); self.step_hor.setReadOnly(True); self.step_hor.setFixedWidth(80)
        self.step_kac = QLineEdit(); self.step_kac.setReadOnly(True); self.step_kac.setFixedWidth(80)
        self.step_comba = QLineEdit(); self.step_comba.setReadOnly(True); self.step_comba.setFixedWidth(80)
        self.step_iter = QLineEdit(); self.step_iter.setReadOnly(True); self.step_iter.setFixedWidth(80)

        res_grid.addWidget(QLabel("<b>Метод</b>"), 0, 0)
        res_grid.addWidget(QLabel("<b>Результат (x)</b>"), 0, 1)
        res_grid.addWidget(QLabel("<b>Шаги</b>"), 0, 2)

        methods = [
            ("Дихотомия:", self.res_dih, self.step_dih),
            ("Хорды:", self.res_hor, self.step_hor),
            ("Касательные:", self.res_kac, self.step_kac),
            ("Комбинированный:", self.res_comba, self.step_comba),
            ("Итерационный:", self.res_iter, self.step_iter)
        ]

        for i, (name, res_field, step_field) in enumerate(methods, 1):
            res_grid.addWidget(QLabel(name), i, 0)
            res_grid.addWidget(res_field, i, 1)
            res_grid.addWidget(step_field, i, 2)

        res_grid.setRowStretch(6, 1)
        res_group.setLayout(res_grid)
        
        mid_side.addWidget(res_group)
        mid_side.addStretch()

        right_side = QVBoxLayout()

        plot_container = QGroupBox("Визуализация")
        plot_layout = QVBoxLayout()
        self.figure = Figure(facecolor='#FFFFFF')
        self.canvas = FCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(True, linestyle='--', alpha=0.6)
        plot_layout.addWidget(self.canvas)
        plot_container.setLayout(plot_layout)
        right_side.addWidget(plot_container, 1)

        content_layout.addLayout(left_side, 2)
        content_layout.addLayout(mid_side, 4) 
        content_layout.addLayout(right_side, 6)
        outer_layout.addLayout(content_layout)
# Класс, которая отвечает за окно с нелинейными уравнениями, графикам и 
# таблицой