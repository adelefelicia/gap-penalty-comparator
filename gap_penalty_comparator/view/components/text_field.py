from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLineEdit


class TextField(QLineEdit):
    """
    Custom input field class for simplified instantiation.
    """
    def __init__(self, width, height, parent=None, placeholder="", font="Arial", font_size=14, mask=""):
        super(TextField, self).__init__(parent)
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.setFont(QFont(font, font_size))
        self.setPlaceholderText(placeholder)
        self.setInputMask(mask)