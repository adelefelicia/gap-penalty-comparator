import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIntValidator
from PyQt6.QtWidgets import QFrame, QScrollArea, QVBoxLayout, QWidget

from .components.button import Button
from .components.label import Label
from .components.text_area import TextArea
from .components.text_field import TextField


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
        submit_btn.setObjectName("submitBtn")
        input_layout.addWidget(submit_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.matrices_frame = QFrame()
        self.matrices_layout = QVBoxLayout()
        self.matrices_frame.setLayout(self.matrices_layout)
        self.matrices_layout.setContentsMargins(20, 0, 20, 0)
        self.matrices_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.matrices_frame.setVisible(False)

        edit_alignment_btn = Button(250, 50, "Edit alignments/penalties", self, font_size=12)
        edit_alignment_btn.clicked.connect(self.show_main_view)
        self.matrices_layout.addWidget(edit_alignment_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.input_frame, stretch=1)  # Stretch keeps title from moving between views
        self.main_layout.addWidget(self.matrices_frame, stretch=1) # Stretch keeps title from moving between views
    
    def display_matrices(self, value_matrices, arrow_matrices, sequences, alignment_coordinates):
        """
        Displays the generated alignment matrices with labels and arrows.

        Args:
            value_matrices (list(np.array)): list of alignment matrices with scores
            arrow_matrices (list(np.array)): list of matrices with values representing arrows for backtracking.
            sequences (tuple): tuple containing the two sequences being aligned
            alignment_coordinates (list(list(int))): nested list of coordinates for positions of the alignment cells
        """
        self.toggle_matrices_view(True)

        num_matrices = len(value_matrices)
        fig_height = max(5, 3 * num_matrices)

        # Keep canvas from shrinking when switching views by deleting it before creating a new one
        if hasattr(self, 'canvas') and self.canvas is not None:
            self.matrices_layout = self.matrices_frame.layout()
            self.matrices_layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

        self.figure, axes = plt.subplots(nrows=num_matrices, figsize=(5, fig_height))
        self.canvas = FigureCanvas(self.figure)

        if num_matrices == 1:
            axes = [axes]

        for i, (val_matrix, ax, arrow_matrix, coordinates) in enumerate(zip(value_matrices, axes, arrow_matrices, alignment_coordinates)):
            ax.clear()

            seq1, seq2 = sequences
            len1, len2 = len(seq1), len(seq2)

            display_matrix = self.add_sequence_labels(val_matrix, seq1, seq2)
            
            # Add arrows to matrix
            # for r in range(len1):
            #     for c in range(len2):
            #         arrow_symbols = []
            #         if arrows[r][c] == 1:
            #             arrow_symbols.append("↖")
            #         if arrows[r][c] == 2:
            #             arrow_symbols.append("↑")
            #         if arrows[r][c] == 3:
            #             arrow_symbols.append("←")
            #         if arrow_symbols:
            #             display_matrix[r + 1][c + 1] = str(display_matrix[r + 1][c + 1]) + " " + "".join(arrow_symbols)

            table = ax.table(cellText=display_matrix, loc='center', cellLoc='center', bbox=[0, 0, 1, 1])
            self.format_matrix_cells(table, coordinates)
                    
            ax.axis('off')
            # ax.set_aspect('equal') # TODO decide if it should be always square or always rectangular
            ax.set_title(f"Generated Matrix {i + 1}", fontsize=16) # TODO add penalty title

        self.figure.tight_layout()

        self.canvas.setFixedSize(int(self.figure.get_size_inches()[0] * 150), int(fig_height * 150))
        self.matrices_layout.addWidget(self.canvas, alignment=Qt.AlignmentFlag.AlignCenter)
        self.canvas.draw()

    def add_sequence_labels(self, value_matrix, seq1, seq2):
        """ Adds the characters of the sequences to the display matrix' first row and column.
            Leaves the first two elements in the first row and column blank."""
        display_matrix = [[''] + [''] + list(seq2)]
        for row_idx, row in enumerate(value_matrix):
            seq1_char = ''
            if row_idx > 0 and row_idx <= len(seq1) + 1:
                seq1_char = seq1[row_idx - 2]
            display_matrix.append([seq1_char] + row.tolist())
        
        return display_matrix

    def format_matrix_cells(self, table, alignment_coordinates):
        for key, cell in table.get_celld().items():
                row, col = key
                if row == 0 or col == 0:
                    cell.set_text_props(weight='bold')
                    cell.set_facecolor('#cccccc')
                elif row == 1 and col == 1:
                        cell.set_facecolor('#0ceb6f')
                elif (row - 1, col - 1) in alignment_coordinates:
                    cell.set_facecolor('#85e6b0') 

    def show_main_view(self):
        self.toggle_matrices_view(False)

    def toggle_matrices_view(self, show_matrices):
        """
        Toggles between the input view and the matrix view.

        Args:
            show_matrices (bool): If True, show the matrix view; otherwise, show the input view.
        """
        self.helper_text.setVisible(not show_matrices)
        self.input_frame.setVisible(not show_matrices)
        self.matrices_frame.setVisible(show_matrices)
    
    def get_sequences(self):
        return self.input_seq1.toPlainText(), self.input_seq2.toPlainText()

    def get_gap_penalties(self):
        penalties = [self.gap_penalty1.text(), self.gap_penalty2.text(), self.gap_penalty3.text()]
        return [int(p) for p in penalties if p.strip()]
