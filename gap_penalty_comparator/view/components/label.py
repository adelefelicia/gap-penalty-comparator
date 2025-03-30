from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel


class Label(QLabel):
    """
    Custom label class for simplified label instantiation.
    """
    def __init__(self, text, parent=None, font="Arial", font_size=14, weight=QFont.Weight.Normal, alignment=None):
        super(Label, self).__init__(parent)
        self.setText(text)
        self.setFont(QFont(font, font_size, weight))
        if alignment:
            self.setAlignment(alignment)