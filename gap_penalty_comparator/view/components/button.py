from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton


class Button(QPushButton):
    """
    Custom button class for simplified instantiation.
    """
    def __init__(self, width, height, label, parent=None, font="Arial", font_size=14):
        super(Button, self).__init__(parent)
        self.setText(label)
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.setFont(QFont(font, font_size))