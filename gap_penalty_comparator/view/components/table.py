from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class Table(QWidget):
    """
    Custom table class using QLabel and QGridLayout to mimic a table.
    """

    def __init__(self, horizontal_headers, vertical_headers, items, parent=None):
        super().__init__(parent)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        bold_font = QFont()
        bold_font.setBold(True)

        # Top-left empty corner
        corner = QLabel("")
        corner.setStyleSheet(self._cell_style())
        self.layout.addWidget(corner, 0, 0)

        # Horizontal headers
        for col, header in enumerate(horizontal_headers):
            label = QLabel(header)
            label.setFont(bold_font)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet(self._cell_style())
            self.layout.addWidget(label, 0, col + 1)

        for row, row_data in enumerate(items):
            # Vertical header
            header = QLabel(vertical_headers[row])
            header.setFont(bold_font)
            header.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header.setStyleSheet(self._cell_style())
            self.layout.addWidget(header, row + 1, 0)

            # Table content
            for col, value in enumerate(row_data):
                cell = QLabel(str(value))
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setStyleSheet(self._cell_style())
                self.layout.addWidget(cell, row + 1, col + 1)

    def _cell_style(self):
        return """
            QLabel {
                border: 1px solid #444;
                padding: 6px;
            }
        """
