from Style.Setteng_style import IW
# Импорт настроек пользовательского интерфейса

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QGroupBox,
                             QFormLayout, QLabel, QTableWidget, 
                             QHeaderView as QHV)
from PyQt6.QtGui import QIcon
# Импорт компонентов библиотеки PyQt6 для работы с графическим интерфейсом

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FCanvas
from matplotlib.figure import Figure
# Импорт библиотеки для работы с графиками

class PolyWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Интерполяция")
        self.setMinimumSize(1350, 850)
        self.setStyleSheet(IW)
        self.active_hint = None
        self.setWindowIcon(QIcon("Icon/Poly/Poly_icon.png"))
        self.init_ui()

    def init_ui(self):
        from Function.Validation.ui_poly import (add_point, 
                                                 fill_by_condition,
                                                delete_selected, clear_all, 
                                                run_interpolation, rex_float,
                                                live_validation as l_v,
                                                update_button_state)

        outer_layout = QVBoxLayout(self)
        content_layout = QHBoxLayout()
        left_side = QVBoxLayout()

        interp_group = QGroupBox("Точка для интерполяции")
        interp_form = QFormLayout()
        self.input_interp_x = QLineEdit("0.1")
        self.input_interp_x.setValidator(rex_float)
        interp_form.addRow("Введите x<sup>*</sup>:", self.input_interp_x)
        interp_group.setLayout(interp_form)
        left_side.addWidget(interp_group)

        node_group = QGroupBox("Добавление узлов")
        node_form = QFormLayout()
        self.input_x = QLineEdit("1"); 
        self.input_x.setValidator(rex_float)
        self.input_y = QLineEdit("2"); 
        self.input_y.setValidator(rex_float)
        node_form.addRow("Координата X:", self.input_x)
        node_form.addRow("Координата Y:", self.input_y)
        self.btn_add = QPushButton("Добавить точку")
        self.btn_fill = QPushButton("Заполнить по условию")
        node_vbox = QVBoxLayout()
        node_vbox.setSpacing(5)
        node_vbox.addLayout(node_form)
        node_vbox.addWidget(self.btn_add)
        node_vbox.addWidget(self.btn_fill)
        node_group.setLayout(node_vbox)
        left_side.addWidget(node_group)

        ctrl_group = QGroupBox("Управление")
        ctrl_vbox = QVBoxLayout()
        ctrl_vbox.setSpacing(5)
        self.btn_delete = QPushButton("Удалить выбранную")
        self.btn_clear = QPushButton("Очистить всё")
        self.btn_exit = QPushButton("Выход")
        ctrl_vbox.addWidget(self.btn_delete)
        ctrl_vbox.addWidget(self.btn_clear)
        ctrl_vbox.addWidget(self.btn_exit)
        ctrl_group.setLayout(ctrl_vbox)
        left_side.addWidget(ctrl_group)
        left_side.addStretch()

        mid_side = QVBoxLayout()
        table_group = QGroupBox("Табличные данные")
        table_layout = QVBoxLayout()
        self.table_points = QTableWidget(0, 2)
        self.table_points.setHorizontalHeaderLabels(["X", "Y"])
        self.table_points.horizontalHeader()\
            .setSectionResizeMode(QHV.ResizeMode.Stretch)
        table_layout.addWidget(self.table_points)
        table_group.setLayout(table_layout)
        mid_side.addWidget(table_group, 3)

        res_group = QGroupBox("Значение полинома в точке интерполяции")
        res_form = QFormLayout()
        self.res_lagrange = QLineEdit(); 
        self.res_lagrange.setReadOnly(True)
        self.res_newton = QLineEdit(); 
        self.res_newton.setReadOnly(True)
        self.res_canonical = QLineEdit(); 
        self.res_canonical.setReadOnly(True)
        self.label_formula = QLabel("Универсальная формула: ")
        self.label_formula.setWordWrap(True)
        res_form.addRow("Лагранжа:", self.res_lagrange)
        res_form.addRow("Ньютона:", self.res_newton)
        res_form.addRow("Канонический:", self.res_canonical)
        res_form.addRow(self.label_formula)
        res_group.setLayout(res_form)
        mid_side.addWidget(res_group, 2)

        right_side = QVBoxLayout()
        plot_container = QGroupBox("График P(x) и табличные точки")
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

        self.input_x.textChanged.connect(lambda text: l_v(self, 1))
        self.input_y.textChanged.connect(lambda text: l_v(self, 1))
        self.input_interp_x.textChanged.connect(lambda text: l_v(self, 2))

        self.btn_add.clicked.connect(lambda: add_point(self))
        self.btn_fill.clicked.connect(lambda: fill_by_condition(self))
        self.btn_delete.clicked.connect(lambda: delete_selected(self))
        self.btn_clear.clicked.connect(lambda: clear_all(self))
        self.btn_exit.clicked.connect(self.close)
        update_button_state(self)
# Класс, которая отвечает за окно интерполяции, графикам и таблицой