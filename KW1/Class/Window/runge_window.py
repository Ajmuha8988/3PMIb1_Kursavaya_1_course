from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QRadioButton, QGroupBox,
                             QGridLayout)
from PyQt6.QtCore import QTimer, Qt, QSize
from PyQt6.QtGui import QIcon
# Импорт компонентов библиотеки PyQt6 для работы с графическим интерфейсом

import os
# Библиотека для работы со встроенным интерпретатором

from Style.Setteng_style import (Runge_QGroupBox, Integral_QGroupBox, IW,
                                 Label_epc, Input_epc, Headers_Runge_Table,
                                 Row_Method_Table)
# Импорт настроек пользовательского интерфейса

class RungeWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Правило Рунге")
        self.setFixedSize(820, 620)
        self.init_ui()

    def init_ui(self):
        from Function.Integral_operation import calculate_runge_logic
        from Function.ui import rex_epc, live_validation

        main_layout = QVBoxLayout(self)
        
        top_group = QGroupBox("правило рунге")
        top_group.setStyleSheet(Runge_QGroupBox)
        
        grid = QGridLayout()
        grid.setContentsMargins(15, 25, 15, 15)
        grid.setSpacing(8)

        grid.setColumnMinimumWidth(0, 140)

        lbl_acc = QLabel("точность")
        lbl_acc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_acc.setStyleSheet(Label_epc)
        grid.addWidget(lbl_acc, 0, 0)
        
        self.eps_input = QLineEdit("0.00001")
        self.eps_input.textChanged.connect(lambda: live_validation(self, 2))
        self.eps_input.setValidator(rex_epc)
        self.eps_input.setFixedWidth(140)
        self.eps_input.setStyleSheet(Input_epc)
        grid.addWidget(self.eps_input, 0, 1)

        headers = ["n", "2n", "n ="]
        for col, text in enumerate(headers, 1):
            lbl = QLabel(text)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(Headers_Runge_Table)
            grid.addWidget(lbl, 1, col)

        self.res_rows = {}
        
        methods = [("s левые", "left"), ("s правые", "right"), 
                   ("s трап", "trap"), ("s симпс", "simp")]

        for i, (name, key) in enumerate(methods):
            lbl = QLabel(name); 
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter); 
            lbl.setStyleSheet(Row_Method_Table)
            grid.addWidget(lbl, i + 2, 0)
            
            f_n = QLineEdit(); 
            f_n.setReadOnly(True); 
            f_n.setAlignment(Qt.AlignmentFlag.AlignCenter)
            f_2n = QLineEdit(); 
            f_2n.setReadOnly(True); 
            f_2n.setAlignment(Qt.AlignmentFlag.AlignCenter)
            f_fin = QLineEdit(); 
            f_fin.setReadOnly(True); 
            f_fin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            grid.addWidget(f_n, i + 2, 1); 
            grid.addWidget(f_2n, i + 2, 2); 
            grid.addWidget(f_fin, i + 2, 3)
            self.res_rows[key] = {"n_edit": f_n, "n2_edit": f_2n, 
                                  "final_n_edit": f_fin}

        top_group.setLayout(grid)
        main_layout.addWidget(top_group)

        bottom_layout = QHBoxLayout()

        int_group = QGroupBox("интеграл")
        int_group.setStyleSheet(Integral_QGroupBox)
        int_vbox = QVBoxLayout()
        
        self.radio_group = []
        c_f_p = os.path.abspath(__file__) 
        p_root = os.path.dirname(os.path.dirname(os.path.dirname(c_f_p)))

        icon_dir = os.path.join(p_root, "icon") 

        integral_names = ["Integral1", "Integral2", "Integral3", "Integral4"]
        for i, name in enumerate(integral_names):
            rb = QRadioButton("")
            rb.setIconSize(QSize(180, 45)) 
            rb.setMinimumHeight(55)

            icon_path = os.path.join(icon_dir, f"{name}.png")
    
            if os.path.exists(icon_path):
                rb.setIcon(QIcon(icon_path))
            else:
                print(f"Файл не найден: {icon_path}")
            if i == 0: rb.setChecked(True)
            rb.toggled.connect(lambda: live_validation(self, 2))
            int_vbox.addWidget(rb)
            self.radio_group.append(rb)
        
        int_group.setLayout(int_vbox)
        bottom_layout.addWidget(int_group, 3)

        btn_vbox = QVBoxLayout()
        btn_vbox.setSpacing(10)
        btn_vbox.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.btn_find = QPushButton("найти"); 
        self.btn_exit = QPushButton("выход");
        
        for b in [self.btn_find, self.btn_exit]:
            b.setStyleSheet(IW)
            btn_vbox.addWidget(b)

        bottom_layout.addStretch(1)
        bottom_layout.addLayout(btn_vbox)
        main_layout.addLayout(bottom_layout)

        self.btn_find.clicked.connect(lambda: calculate_runge_logic(self))
        self.btn_exit.clicked.connect(self.close)
        QTimer.singleShot(50, lambda: live_validation(self, 2))
# Класс, хранящая окно с интегралами и отвечающая за выполнения вычисления
# погрешности правилом Рунге