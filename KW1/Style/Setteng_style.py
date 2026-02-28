IW = ("""
    QDialog { 
        background-color: #F0F8FF; 
    }
    
    QWidget { 
        color: #333333; 
        font-family: 'Segoe UI', Arial, sans-serif; 
        font-size: 14px;
    }

    #TitleLabel { 
        font-size: 24px; 
        font-weight: bold; 
        color: #4A00E0; 
        padding: 10px; 
        margin-bottom: 10px; 
        border-bottom: 3px solid #00BFFF; 
    }

    QGroupBox {
        font-weight: bold;
        border: 2px solid #D3D3D3;
        border-radius: 10px;
        margin-top: 15px;
        padding-top: 15px;
        background-color: white;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 15px;
        padding: 0 5px;
        color: #4A00E0;
    }

    QLineEdit {
        border: 1px solid #D3D3D3;
        border-radius: 5px;
        padding: 8px;
        background: #FFFFFF;
        selection-background-color: #00BFFF;
    }
    
    QLineEdit:focus {
        border: 2px solid #00BFFF;
    }

    QPushButton { 
        background-color: #00BFFF; 
        color: white; 
        border-radius: 8px; 
        padding: 10px 20px; 
        font-size: 15px; 
        font-weight: bold; 
        border: none; 
    }
    QPushButton:hover { background-color: #1E90FF; }
    QPushButton:pressed { background-color: #0080FF; }
    QPushButton:disabled { background-color: #A9A9A9; }

    QRadioButton {
        padding: 8px;
        spacing: 15px;
    }
    
    QRadioButton::indicator {
        width: 18px;
        height: 18px;
    }

    QTableWidget {
        gridline-color: #D3D3D3;
        border: 1px solid #D3D3D3;
        border-radius: 5px;
        background-color: white;
    }
    
    QHeaderView::section {
        background-color: #00BFFF;
        color: white;
        padding: 5px;
        font-weight: bold;
        border: none;
    }
""")
# Главный стиль самой программы

MH_style = (
    """
        background-color: #fb7185; 
        color: white; 
        border-radius: 4px; 
        padding: 8px 12px;
        font-size: 12px;
        font-weight: bold;
        border: 1px solid #e11d48;
    """)
# Стиль всплывающей подсказки

Runge_QGroupBox = ("""
        QGroupBox { color: blue; font-weight: bold; border: 1px solid #ccc; 
        margin-top: 15px; }
        QGroupBox::title { subcontrol-origin: margin; left: 10px; 
        padding: 0 5px; }
    """)
# Стиль виджет-контейнера "Правило-Рунге"

Integral_QGroupBox = ("""
        QGroupBox { color: blue; font-weight: bold; border: 1px solid #ccc; }
    """)
# Стиль виджет-контейнера "Интеграл"

Label_epc = ("""
    background-color: #f0f0f0; border: 1px solid #ccc; padding: 5px; color: black; font-weight: bold;
    """)
# Стиль строки "Точность"

Input_epc = ("""
    border: 2px solid #00BFFF; padding: 4px; font-weight: bold;
    """)
# Стиль поля ввода "Точность"

Headers_Runge_Table = ("""
    background-color: #E3F2FD; color: #1976D2; font-weight: bold; border: 1px solid #BBDEFB; padding: 5px;
    """)
# Стиль заголовка таблицы

Row_Method_Table = ("""
    background-color: #f8f8f8; border: 1px solid #ddd; padding: 5px; font-weight: bold;
    """)
# Стиль столбцов наименовании методов
