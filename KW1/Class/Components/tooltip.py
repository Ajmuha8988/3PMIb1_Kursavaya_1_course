from PyQt6.QtWidgets import QLabel, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint
# Импорт компонентов библиотеки PyQt6 для работы с графическим интерфейсом

from Style.Setteng_style import MH_style

class ModernHint(QLabel):
    def __init__(self, parent, text, target_widget):
        super().__init__(text, parent)

        self.setStyleSheet(MH_style)
        
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.adjustSize() 

        global_pos = target_widget.mapToGlobal(QPoint(0, 0))
        local_pos = parent.mapFromGlobal(global_pos)

        center_x = local_pos.x() + (target_widget.width() // 2) - \
            (self.width() // 2)
        top_y = local_pos.y() - self.height() - 8
        
        self.move(center_x, top_y)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(250)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()
        
        self.show()

    def hide_and_delete(self):
        self.anim.setDirection(QPropertyAnimation.Direction.Backward)
        self.anim.finished.connect(self.deleteLater)
        self.anim.start()
# Класс, в котором содержится настройки всплывающего окна