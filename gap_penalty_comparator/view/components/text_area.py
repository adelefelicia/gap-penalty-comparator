from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QTextEdit


class TextArea(QTextEdit):
    """
    Custom text area class for simplified instantiation.
    """
    def __init__(self, width, height, parent=None, placeholder="", font="Arial", font_size=14):
        super(TextArea, self).__init__(parent)
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.setFont(QFont(font, font_size))
        self.setPlaceholderText(placeholder)