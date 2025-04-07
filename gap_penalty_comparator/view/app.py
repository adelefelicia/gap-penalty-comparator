from statistics import fmean

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIntValidator
from PyQt6.QtWidgets import (QApplication, QButtonGroup, QFrame, QHBoxLayout,
                             QMessageBox, QRadioButton, QScrollArea,
                             QVBoxLayout, QWidget)

from .components.button import Button
from .components.label import Label
from .components.table import Table
from .components.text_field import TextField


class MainWindow(QScrollArea):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.showMaximized()
        
        self.gaps = []
    
    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            submit_button = self.findChild(Button, "submitBtn")
            if submit_button and submit_button.isVisible():
                submit_button.click()
        else:
            super().keyPressEvent(event)
    
    def init_ui(self):
        # Main container widget (required to make window scrollable)
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)
        self.setWindowTitle("Gap Penalty Comparator")
        
        title = Label("Gap Penalty Comparator", self, font_size=30, weight=QFont.Weight.Bold, alignment=Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("padding: 30px;")
        self.main_layout.addWidget(title)

        self.helper_text = Label("""
            Compare how different gap penalties impact global alignments for the Needleman-Wunsch algorithm.
                                 
            Choose between BLOSUM62 or identity (-/+ 1 for (mis)match) scoring methods.
            Enter two sequences and three gap penalties to generate the alignment matrices and compare
            the results.
        """, self, alignment=Qt.AlignmentFlag.AlignCenter)
        self.helper_text.setWordWrap(True)
        self.main_layout.addWidget(self.helper_text)
        
        self.input_frame = QFrame()
        input_layout = QVBoxLayout()
        self.input_frame.setLayout(input_layout)
        input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        radio_frame = QFrame()
        radio_layout = QHBoxLayout()
        radio_frame.setLayout(radio_layout)
        radio_layout.addWidget(Label("Scoring method:", self, font_size=12))

        # Scoring method radio buttons
        self.radio_blosum = QRadioButton("BLOSUM62", self)
        self.radio_identity = QRadioButton("Identity", self)
        self.radio_identity.setChecked(True)
        self.radio_group = QButtonGroup(self)
        self.radio_group.addButton(self.radio_blosum)
        self.radio_group.addButton(self.radio_identity)
        radio_layout.addWidget(self.radio_blosum)
        radio_layout.addWidget(self.radio_identity)
        input_layout.addWidget(radio_frame)
        
        # Sequence inputs
        self.input_seq1 = TextField(600, 50, self, "Enter first sequence")
        input_layout.addWidget(self.input_seq1)
        input_layout.addSpacing(10)
        self.input_seq2 = TextField(600, 50, self, "Enter second sequence")
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

        input_layout.addSpacing(30)
        submit_btn = Button(350, 70, "Calculate alignment matrix", self)
        submit_btn.setObjectName("submitBtn")
        input_layout.addWidget(submit_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        input_layout.addStretch()

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
    
    def display_matrices(self, value_matrices, arrow_matrices, sequences, alignment_coordinates, gap_penalties):
        """
        Displays the generated alignment matrices with labels and arrows.

        Args:
            value_matrices (list(np.array)): list of alignment matrices with scores
            arrow_matrices (list(np.array)): list of matrices with values representing arrows for backtracking.
            sequences (tuple): tuple containing the two sequences being aligned
            alignment_coordinates (list(list(int))): nested list of coordinates for positions of the alignment cells
        """
        seq1, seq2 = sequences
        self.toggle_matrices_view(True)
        self.matrices_layout.removeWidget(self.table) if hasattr(self, 'table') else None
        self.create_and_populate_table()

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

            display_matrix = self.add_sequence_labels(val_matrix, seq1, seq2)
            self.overlay_arrows(arrow_matrix, display_matrix)

            table = ax.table(cellText=display_matrix, loc='center', cellLoc='center', bbox=[0, 0, 1, 1])
            self.format_matrix_cells(table, coordinates)
                    
            ax.axis('off')
            ax.set_title(f"Gap penalty = {gap_penalties[i]}", fontsize=16) # TODO add penalty title

        self.figure.tight_layout()

        max_seq_length = max(len(sequences[0]), len(sequences[1]))

        # Quadratic scaling function for the canvas size
        calculated_width = int(self.figure.get_size_inches()[0] * (50 + 0.5 * max_seq_length ** 2))
        calculated_height = int(fig_height * (200 + 0.5 * max_seq_length ** 2))

        min_width = int(self.figure.get_size_inches()[0] * 150)
        min_height = int(fig_height * 150)

        screen_geometry = QApplication.primaryScreen().availableGeometry()
        max_width = screen_geometry.width()
        max_height = screen_geometry.height()

        # Clamp the width and height to the specified interval
        width = max(min_width, min(calculated_width, max_width))
        height = max(min_height, min(calculated_height, max_height))

        self.canvas.setFixedSize(width, height)
        self.matrices_layout.addWidget(self.canvas, alignment=Qt.AlignmentFlag.AlignCenter)
        self.canvas.draw()

    
    def overlay_arrows(self, arrow_matrix, display_matrix):
        """Adds arrows to the cell text in the display matrix."""
        for r, row in enumerate(display_matrix):
            for c, _ in enumerate(row):
                if r == 0 or c == 0:
                    continue
                arrows = arrow_matrix[r - 1][c - 1]
                arrow_symbols = ""
                if 3 in arrows:
                    arrow_symbols += "←"
                if 1 in arrows:
                    arrow_symbols += "↖"
                if 2 in arrows:
                    arrow_symbols += "↑"
                display_matrix[r][c] = f"{arrow_symbols}\n{int(display_matrix[r][c])}"


    def add_sequence_labels(self, value_matrix, seq1, seq2):
        """ Adds the characters of the sequences to the display matrix' first row and column.
            Leaves the first two elements in the first row and column blank."""
        display_matrix = [[''] + [''] + list(seq2)]
        for row_idx, row in enumerate(value_matrix):
            seq1_char = ''
            if row_idx > 0 and row_idx <= len(seq1) + 1:
                seq1_char = seq1[row_idx - 1]
            display_matrix.append([seq1_char] + row.tolist())
        
        return display_matrix

    def format_matrix_cells(self, table, alignment_coordinates):
        max_font_size = 16 
        min_font_size = 8

        # Dynamically calculate font size (inverse proportionality)
        font_size = max(min_font_size, min(max_font_size, int(100 / (len(alignment_coordinates) + 1))))

        for key, cell in table.get_celld().items():
                row, col = key
                if row == 0 or col == 0:
                    cell.set_text_props(weight='bold')
                    cell.set_facecolor('#cccccc')
                elif row == 1 and col == 1:
                        cell.set_facecolor('#0ceb6f')
                elif (row - 1, col - 1) in alignment_coordinates:
                    cell.set_facecolor('#85e6b0')
                cell.set_text_props(fontsize=font_size)

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
    
    def popup_dialog(self, message, dialog_type):
        """Displays an error dialog with the given message."""
        popup_dialog = QMessageBox(self)
        if dialog_type == "info":
            popup_dialog.setIcon(QMessageBox.Icon.Information)
            popup_dialog.setWindowTitle("Information")
        elif dialog_type == "warning":
            popup_dialog.setIcon(QMessageBox.Icon.Warning)
            popup_dialog.setWindowTitle("Warning")
        elif dialog_type == "error":
            popup_dialog.setIcon(QMessageBox.Icon.Critical)
            popup_dialog.setWindowTitle("Error")

        popup_dialog.setText(message)
        popup_dialog.exec()
    
    def loading_cursor(self, loading):
        if loading:
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        else:
            QApplication.restoreOverrideCursor()

    def mean_or_zero(self, gaps):
        """Returns the mean of the gaps or 0 if there are no gaps."""
        return round(fmean(gaps), 1) if gaps else 0

    def create_and_populate_table(self):
        """Populates the table with the given items."""
        self.table = Table(["Num of gaps", "Avg. gap length"],
                            [f"Penalty={self.gap_penalty1.text()}",
                             f"Penalty={self.gap_penalty2.text()}",
                             f"Penalty={self.gap_penalty3.text()}"],
                             [[len(self.gaps[0]), self.mean_or_zero(self.gaps[0])],
                                [len(self.gaps[1]), self.mean_or_zero(self.gaps[1])],
                                [len(self.gaps[2]), self.mean_or_zero(self.gaps[2])]],
                            self)
        self.table.setMaximumWidth(400)
        self.matrices_layout.addWidget(self.table, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def get_sequences(self):
        return self.input_seq1.text(), self.input_seq2.text()

    def get_gap_penalties(self):
        penalties = [self.gap_penalty1.text(), self.gap_penalty2.text(), self.gap_penalty3.text()]
        return [int(p) for p in penalties if p.strip()]
    
    def set_gaps(self, gaps):
        self.gaps = gaps
    
    def get_scoring_method(self):
        """
        Returns the currently selected scoring method.
        """
        if self.radio_blosum.isChecked():
            return "BLOSUM62"
        elif self.radio_identity.isChecked():
            return "Identity"
        return None
