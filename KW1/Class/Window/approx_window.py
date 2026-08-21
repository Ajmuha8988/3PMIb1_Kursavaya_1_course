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

class ApproxWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Аппроксимация")
        self.setMinimumSize(1350, 850)
        self.setStyleSheet(IW)
        self.active_hint = None
        self.setWindowIcon(QIcon("Icon/Approx/approximation.png"))
        self.init_ui()

    def init_ui(self):
        from Function.Validation.ui_approx import (add_point, 
                               fill_by_condition,
                               delete_selected, clear_all, 
                               rex_float,live_validation as l_v,
                               update_button_state)

        outer_layout = QVBoxLayout(self)
        content_layout = QHBoxLayout()
        left_side = QVBoxLayout()

        node_group = QGroupBox("Добавление узлов")
        node_form = QFormLayout()
        self.input_x = QLineEdit("1") 
        self.input_x.setValidator(rex_float)
        self.input_y = QLineEdit("2") 
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

        table_group = QGroupBox("Табличные данные")
        table_layout = QVBoxLayout()
        self.table_points = QTableWidget(0, 2)
        self.table_points.setHorizontalHeaderLabels(["X", "Y"])
        self.table_points.horizontalHeader()\
            .setSectionResizeMode(QHV.ResizeMode.Stretch)
        table_layout.addWidget(self.table_points)
        table_group.setLayout(table_layout)
        left_side.addWidget(table_group, 1)

        mid_side = QVBoxLayout()
        res_group = QGroupBox("Результаты аппроксимации МНК")
        res_form = QFormLayout()
        
        self.res_lin_a = QLineEdit() 
        self.res_lin_b = QLineEdit() 
        self.res_lin_sse = QLineEdit() 
        self.res_lin_a.setReadOnly(True)
        self.res_lin_b.setReadOnly(True)
        self.res_lin_sse.setReadOnly(True)
        
        self.res_quad_a = QLineEdit() 
        self.res_quad_b = QLineEdit() 
        self.res_quad_c = QLineEdit() 
        self.res_quad_sse = QLineEdit() 
        self.res_quad_a.setReadOnly(True)
        self.res_quad_b.setReadOnly(True)
        self.res_quad_c.setReadOnly(True)
        self.res_quad_sse.setReadOnly(True)
        
        self.res_cust_a = QLineEdit() 
        self.res_cust_b = QLineEdit() 
        self.res_cust_c = QLineEdit() 
        self.res_cust_sse = QLineEdit() 
        self.res_cust_a.setReadOnly(True)
        self.res_cust_b.setReadOnly(True)
        self.res_cust_c.setReadOnly(True)
        self.res_cust_sse.setReadOnly(True)

        res_form.addRow(QLabel("<b>Линейная регрессия:</b>"))
        res_form.addRow("Поле a:", self.res_lin_a)
        res_form.addRow("Поле b:", self.res_lin_b)
        res_form.addRow("Суммарная погрешность:", self.res_lin_sse)

        res_form.addRow(QLabel("<b>Квадратичная регрессия:</b>"))
        res_form.addRow("Поле a:", self.res_quad_a)
        res_form.addRow("Поле b:", self.res_quad_b)
        res_form.addRow("Поле c:", self.res_quad_c)
        res_form.addRow("Суммарная погрешность:", self.res_quad_sse)

        res_form.addRow(QLabel("<b>Пользовательская регрессия:</b>"))
        res_form.addRow("Поле a:", self.res_cust_a)
        res_form.addRow("Поле b:", self.res_cust_b)
        res_form.addRow("Поле c:", self.res_cust_c)
        res_form.addRow("Суммарная погрешность:", self.res_cust_sse)
        
        res_group.setLayout(res_form)
        mid_side.addWidget(res_group, 1)

        right_side = QVBoxLayout()
        plot_container = QGroupBox("График аппроксимации")
        plot_layout = QVBoxLayout()
        self.figure = Figure(facecolor='#FFFFFF')
        self.canvas = FCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(True, linestyle='--', alpha=0.6)
        plot_layout.addWidget(self.canvas)
        plot_container.setLayout(plot_layout)
        right_side.addWidget(plot_container)

        content_layout.addLayout(left_side, 3)
        content_layout.addLayout(mid_side, 3)
        content_layout.addLayout(right_side, 5)
        outer_layout.addLayout(content_layout)

        self.input_x.textChanged.connect(lambda text: l_v(self, 1))
        self.input_y.textChanged.connect(lambda text: l_v(self, 1))

        self.btn_add.clicked.connect(lambda: add_point(self))
        self.btn_fill.clicked.connect(lambda: fill_by_condition(self))
        self.btn_delete.clicked.connect(lambda: delete_selected(self))
        self.btn_clear.clicked.connect(lambda: clear_all(self))
        self.btn_exit.clicked.connect(self.close)
        update_button_state(self)
# Класс, которая отвечает за окно интерполяции, графикам и таблицой