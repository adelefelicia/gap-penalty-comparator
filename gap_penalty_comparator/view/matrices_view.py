import matplotlib.pyplot as plt
from .components.button import Button
from .components.label import Label
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (QFrame, QScrollArea, QVBoxLayout,
                             QWidget)


class MatricesView(QScrollArea):
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

        self.matrices_frame = QFrame()
        self.matrices_frame.setStyleSheet("background-color: blue;") 
        matrices_layout = QVBoxLayout()
        self.matrices_frame.setLayout(matrices_layout)
        matrices_layout.setContentsMargins(20, 0, 20, 0)
        matrices_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        edit_alignment_btn = Button(250, 50, "Edit alignments/penalties", self, font_size=12)
        edit_alignment_btn.clicked.connect(self.controller.show_main_view)
        matrices_layout.addWidget(edit_alignment_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Matplotlib matrix canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: red;")
        matrices_layout.addWidget(self.canvas, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.matrices_frame, stretch=1) # Stretch keeps title from moving between views
    
    def display_matrices(self, value_matrices, arrow_matrices, sequences, alignment_coordinates):
        """
        Displays the generated alignment matrices with labels and arrows.

        Args:
            value_matrices (list(np.array)): list of alignment matrices with scores
            arrow_matrices (list(np.array)): list of matrices with values representing arrows for backtracking.
            sequences (tuple): tuple containing the two sequences being aligned
        """
        print(value_matrices, arrow_matrices, sequences, alignment_coordinates)
        num_matrices = len(value_matrices)
        fig_height = max(5, 3 * num_matrices)

        # self.figure.clear()
        # fig, axes = plt.subplots(nrows=num_matrices, figsize=(5, fig_height))
        # self.figure = fig
        # self.canvas.figure = self.figure

        # Remove the old canvas from the layout
        if hasattr(self, 'canvas') and self.canvas is not None:
            self.main_layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

        # Create a new figure and canvas
        figure, axes = plt.subplots(nrows=num_matrices, figsize=(5, fig_height))
        self.figure = figure
        self.canvas = FigureCanvas(self.figure)

        if num_matrices == 1:
            axes = [axes]

        for i, (val_matrix, ax, arrow_matrix, coordinates) in enumerate(zip(value_matrices, axes, arrow_matrices, alignment_coordinates)):
            ax.clear()

            seq1, seq2 = sequences
            len1, len2 = len(seq1), len(seq2)

            display_matrix = self.add_sequence_labels(val_matrix, seq1, seq2)

            table = ax.table(cellText=display_matrix, loc='center', cellLoc='center', bbox=[0, 0, 1, 1])
            self.format_matrix_cells(table, coordinates)
                    
            ax.axis('off')
            # ax.set_aspect('equal') # TODO decide if it should be always square or always rectangular
            ax.set_title(f"Generated Matrix {i + 1}", fontsize=16) # TODO add penalty title

        self.figure.tight_layout()

        # Add the new canvas to the layout
        self.canvas.setFixedSize(int(self.figure.get_size_inches()[0] * 150), int(fig_height * 150))
        self.main_layout.addWidget(self.canvas, alignment=Qt.AlignmentFlag.AlignCenter)
        self.canvas.draw()

    def add_sequence_labels(self, value_matrix, seq1, seq2):
        """ Adds the characters of the sequences to the display matrix' first row and column.
            Leaves the first two elements in the first row and column blank."""
        display_matrix = [[''] + [''] + list(seq2)]  # Display sequence 2 in the first row
        for row_idx, row in enumerate(value_matrix):
            seq1_char = ''
            if row_idx > 0 and row_idx <= len(seq1) + 1:
                seq1_char = seq1[row_idx - 2]
            display_matrix.append([seq1_char] + row.tolist()) # Add sequence 1 in the first column
        
        return display_matrix

    def format_matrix_cells(self, table, alignment_coordinates):
        for key, cell in table.get_celld().items():
                row, col = key
                if row == 0 or col == 0:  # Sequence headers
                    cell.set_text_props(fontsize=20) # TODO make bigger, no effect rn
                    cell.set_text_props(weight='bold')
                    cell.set_facecolor('#cccccc')
                else:
                    cell.set_fontsize(14)

                    if row == 1 and col == 1: # Start position for alignment
                        cell.set_facecolor('#0ceb6f')

                    elif (row - 1, col - 1) in alignment_coordinates: # Alignment cells
                        cell.set_facecolor('#85e6b0') 

    # def show_main_view(self):
    #     self.hide()
    #     main_view = MainView(self)
    #     main_view.show()

