from .components.button import Button
from .components.label import Label
from .components.text_area import TextArea
from .components.text_field import TextField
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIntValidator
from PyQt6.QtWidgets import (QFrame, QScrollArea, QVBoxLayout,
                             QWidget)


class MainView(QScrollArea):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()
    
    def init_ui(self):
        self.resize(1000, 1000)

        # Main container widget (required to make window scrollable)
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)
        self.setWindowTitle("Gap Penalty Comparator")
        self.setStyleSheet("background-color: white")
        
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
        # submit_btn.setObjectName("submitBtn")
        submit_btn.clicked.connect(self.controller.show_matrices_view)
        input_layout.addWidget(submit_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.input_frame, stretch=1)  # Stretch keeps title from moving between views

    # def show_matrices_view(self):
    #     self.hide()
    #     matrices_view = MatricesView(self)
    #     matrices_view.show()
    
    def get_sequences(self):
        return self.input_seq1.toPlainText(), self.input_seq2.toPlainText()

    def get_gap_penalties(self):
        penalties = [self.gap_penalty1.text(), self.gap_penalty2.text(), self.gap_penalty3.text()]
        return [int(p) for p in penalties if p.strip()]
