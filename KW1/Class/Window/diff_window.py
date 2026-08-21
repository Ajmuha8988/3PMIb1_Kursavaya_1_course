import Function.Validation.ui_diff as ui_diff
# Импорт внешних интерфейсных функций

from Style.Setteng_style import IW
# Импорт настроек пользовательского интерфейса

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QGroupBox,
                             QFormLayout, QLabel, QTableWidget, 
                             QHeaderView as QHV, QRadioButton)
from PyQt6.QtGui import QIcon, QIntValidator, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
# Импорт компонентов библиотеки PyQt6 для работы с графическим интерфейсом

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FCanvas
from matplotlib.figure import Figure
# Импорт библиотеки для работы с графиками

class DiffWindow(QDialog):
    live_validation = ui_diff.live_validation
    update_button_state = ui_diff.update_button_state
    show_single_hint = ui_diff.show_single_hint
    clear_hint = ui_diff.clear_hint
    fill_by_condition = ui_diff.fill_by_condition
    clear_all = ui_diff.clear_all
    run_calculation = ui_diff.run_calculation

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Метод Конечных Разностей")
        self.setMinimumSize(1350, 850)
        self.setStyleSheet(IW)
        self.active_hint = None
        self.setWindowIcon(QIcon("Icon/Diff/differentiation.png"))
        self.init_ui()

    def init_ui(self):
        float_re = QRegularExpression(r"^-?\d*[.,]?\d*$")
        rex_float = QRegularExpressionValidator(float_re)

        outer_layout = QVBoxLayout(self)
        content_layout = QHBoxLayout()
        
        left_side = QVBoxLayout()
        param_group = QGroupBox("Параметры задачи")
        param_form = QFormLayout()

        self.input_px = QLineEdit("1")
        self.input_qx = QLineEdit("-x")
        self.input_fx = QLineEdit("x^2")
        
        self.input_x_start = QLineEdit("0")
        self.input_x_start.setValidator(rex_float)
        
        self.input_y_start = QLineEdit("1")
        self.input_y_start.setValidator(rex_float)
        
        self.input_x_end = QLineEdit("1")
        self.input_x_end.setValidator(rex_float)
        
        self.input_y_end = QLineEdit("2")
        self.input_y_end.setValidator(rex_float)
        
        self.input_n = QLineEdit("3")
        self.input_n.setValidator(QIntValidator(3, 10000))

        lbl_x_start = QLabel("x<sub>нач</sub>:")
        lbl_y_start = QLabel("y(x<sub>нач</sub>):")
        lbl_x_end = QLabel("x<sub>конеч</sub>:")
        lbl_y_end = QLabel("y(x<sub>конеч</sub>):")

        param_form.addRow("p(x):", self.input_px)
        param_form.addRow("q(x):", self.input_qx)
        param_form.addRow("f(x):", self.input_fx)
        param_form.addRow(lbl_x_start, self.input_x_start)
        param_form.addRow(lbl_y_start, self.input_y_start)
        param_form.addRow(lbl_x_end, self.input_x_end)
        param_form.addRow(lbl_y_end, self.input_y_end)
        param_form.addRow("n:", self.input_n)

        self.btn_fill = QPushButton("Заполнить по условию")
        self.btn_calc = QPushButton("Рассчитать")
        
        method_layout = QVBoxLayout()
        method_layout.setSpacing(4)
        method_label = QLabel("Метод решения:")
        self.radio_thomas = QRadioButton("Прогонка")
        self.radio_matrix = QRadioButton("Матричный")
        self.radio_gauss = QRadioButton("Гаусса")
        self.radio_cramer = QRadioButton("Крамера")
        
        self.radio_thomas.setChecked(True)
        
        method_layout.addWidget(method_label)
        method_layout.addWidget(self.radio_thomas)
        method_layout.addWidget(self.radio_matrix)
        method_layout.addWidget(self.radio_gauss)
        method_layout.addWidget(self.radio_cramer)

        param_vbox = QVBoxLayout()
        param_vbox.addLayout(param_form)
        param_vbox.addWidget(self.btn_fill)
        param_vbox.addSpacing(10)
        param_vbox.addLayout(method_layout)
        param_vbox.addSpacing(10)
        param_vbox.addWidget(self.btn_calc)
        param_group.setLayout(param_vbox)
        
        left_side.addWidget(param_group)
        
        self.btn_exit = QPushButton("Выход")
        left_side.addStretch()
        left_side.addWidget(self.btn_exit)

        mid_side = QVBoxLayout()
        res_group = QGroupBox("Результат")
        res_vbox = QVBoxLayout()

        poly_label = QLabel("Интерполяционный полином:")
        self.res_polynomial = QLineEdit()
        self.res_polynomial.setReadOnly(True)

        self.table_results = QTableWidget(0, 2)
        self.table_results.setHorizontalHeaderLabels(["x", "y(x)"])
        self.table_results.horizontalHeader()\
            .setSectionResizeMode(QHV.ResizeMode.Stretch)

        res_vbox.addWidget(poly_label)
        res_vbox.addWidget(self.res_polynomial)
        res_vbox.addWidget(self.table_results)
        res_group.setLayout(res_vbox)
        
        mid_side.addWidget(res_group)

        right_side = QVBoxLayout()
        plot_container = QGroupBox("График решения")
        plot_layout = QVBoxLayout()
        
        self.figure = Figure(facecolor='#FFFFFF')
        self.canvas = FCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(True, linestyle='--', alpha=0.6)
        
        plot_layout.addWidget(self.canvas)
        plot_container.setLayout(plot_layout)
        right_side.addWidget(plot_container)

        content_layout.addLayout(left_side, 2)
        content_layout.addLayout(mid_side, 3)
        content_layout.addLayout(right_side, 5)
        outer_layout.addLayout(content_layout)

        self.btn_fill.clicked.connect(self.fill_by_condition)
        self.btn_calc.clicked.connect(self.run_calculation)
        self.btn_exit.clicked.connect(self.close)

        self.input_x_start.textChanged.connect(lambda: 
                                               self.live_validation(1))
        self.input_x_end.textChanged.connect(lambda: self.live_validation(1))
        self.input_n.textChanged.connect(lambda: self.live_validation(2))
        
        self.input_px.textChanged.connect(self.update_button_state)
        self.input_qx.textChanged.connect(self.update_button_state)
        self.input_fx.textChanged.connect(self.update_button_state)
        self.input_y_start.textChanged.connect(self.update_button_state)
        self.input_y_end.textChanged.connect(self.update_button_state)

        self.update_button_state()
# Класс, отвечающий за окно МКР, графики и таблицу результатов