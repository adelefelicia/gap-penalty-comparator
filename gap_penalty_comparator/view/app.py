import sys

import matplotlib.pyplot as plt
import numpy as np
from components.button import Button
from components.label import Label
from components.text_area import TextArea
from components.text_field import TextField
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIntValidator
from PyQt6.QtWidgets import (QApplication, QFrame, QScrollArea, QVBoxLayout,
                             QWidget)


class MainWindow(QScrollArea):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.resize(1000, 1000)

        # Main container widget (required to make window scrollable)
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)
        
        title = Label("Gap Penalty Comparator", self, font_size=20, weight=QFont.Weight.Bold, alignment=Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("padding: 20px;")
        self.main_layout.addWidget(title)

        self.helper_text = Label("""
            Compare how different gap penalties impact global alignments in the Needleman-Wunsch algorithm.
            Enter two sequences and at least two gap penalties to generate the alignment matrices.
        """, self, alignment=Qt.AlignmentFlag.AlignCenter)
        self.helper_text.setWordWrap(True)
        self.main_layout.addWidget(self.helper_text)
        
        self.input_frame = QFrame()
        input_layout = QVBoxLayout()
        self.input_frame.setLayout(input_layout)
        input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Sequence inputs
        self.input_seq1 = TextArea(400, 150, self, "Enter first sequence")
        input_layout.addWidget(self.input_seq1)
        input_layout.addSpacing(10)
        self.input_seq2 = TextArea(400, 150, self, "Enter second sequence")
        input_layout.addWidget(self.input_seq2)
        input_layout.addSpacing(30)

        # Gap penalty inputs
        self.gap_penalty_layout = QVBoxLayout()
        self.gap_penalty_label = Label("Enter gap penalty values:", self)
        self.gap_penalty_layout.addWidget(self.gap_penalty_label)
        input_layout.addLayout(self.gap_penalty_layout)
        self.gap_penalty1 = TextField(100, 50, self)
        self.gap_penalty1.setValidator(QIntValidator(-99, 0))
        self.gap_penalty_layout.addWidget(self.gap_penalty1)
        self.gap_penalty2 = TextField(100, 50, self)
        self.gap_penalty2.setValidator(QIntValidator(-99, 0))
        self.gap_penalty_layout.addWidget(self.gap_penalty2)
        self.gap_penalty3 = TextField(100, 50, self)
        self.gap_penalty3.setValidator(QIntValidator(-99, 0))
        self.gap_penalty_layout.addWidget(self.gap_penalty3)

        submit_btn = Button(350, 70, "Calculate alignment matrix", self)
        submit_btn.clicked.connect(self.generate_matrix)
        input_layout.addWidget(submit_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.matrices_frame = QFrame()
        matrices_layout = QVBoxLayout()
        self.matrices_frame.setLayout(matrices_layout)
        matrices_layout.setContentsMargins(20, 0, 20, 0)
        matrices_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.matrices_frame.setVisible(False)
        
        # Matplotlib matrix canvas
        self.figure, self.ax = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumSize(500, 500)
        matrices_layout.addWidget(self.canvas, alignment=Qt.AlignmentFlag.AlignCenter)

        edit_alignment_btn = Button(350, 70, "Edit alignments/penalties", self)
        edit_alignment_btn.clicked.connect(self.show_main_view)
        matrices_layout.addWidget(edit_alignment_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.input_frame, stretch=1)  # Stretch keeps title from moving between views
        self.main_layout.addWidget(self.matrices_frame, stretch=1) # Stretch keeps title from moving between views

    def generate_matrix(self):
        # Placeholder for matrix
        max_length = max(len(self.input_seq1.toPlainText()), len(self.input_seq2.toPlainText()))
        matrix_size = max_length if max_length > 0 else 5
        matrix = np.random.randint(1, 100, (matrix_size, matrix_size))

        # Hide input view
        self.helper_text.setVisible(False)
        self.input_frame.setVisible(False)

        # Show matrices view
        self.matrices_frame.setVisible(True)
        self.ax.clear()
        self.ax.table(cellText=matrix, loc='center', cellLoc='center', bbox=[0, 0, 1, 1])
        self.ax.axis('off')
        self.ax.set_title("Generated Matrix", fontsize=16)

        self.canvas.draw()

    def show_main_view(self):
        # Hide matrix view
        self.matrices_frame.setVisible(False)

        # Show input view
        self.helper_text.setVisible(True)
        self.input_frame.setVisible(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Gap Penalty Comparator")
    window.setStyleSheet("background-color: white")
    window.show()
    sys.exit(app.exec())
