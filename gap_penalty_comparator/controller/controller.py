import sys

from model.comparator import backtrack_global_alignment, needleman_wunsch
from PyQt6.QtWidgets import QApplication, QPushButton
from view.app import MainWindow


class Controller:
    def __init__(self):
        self.app = QApplication([])
        self.view = MainWindow()
        
        self.view.findChild(QPushButton, "submitBtn").clicked.connect(self.run_algorithm)

    def run_algorithm(self):
        """Fetches inputs from the view, runs the algorithm, and updates the view with results."""
        seq1, seq2 = self.view.get_sequences() # TODO parse sequences
        gap_penalties = self.view.get_gap_penalties()

        # if len(gap_penalties) < 2:
        #     print("Please enter at least two gap penalties!")  # TODO Replace with proper error handling
        #     return


        value_matrices = []
        arrow_matrices = []
        alignment_coordinates = []

        for penalty in gap_penalties:
            val_matrix, arrow_matrix = needleman_wunsch(seq1, seq2, penalty)
            coordinate_list = backtrack_global_alignment(seq1, seq2, arrow_matrix)

            value_matrices.append(val_matrix)
            arrow_matrices.append(arrow_matrix)
            alignment_coordinates.append(coordinate_list)

        self.view.display_matrices(value_matrices, arrow_matrices, (seq1, seq2), alignment_coordinates) 

    def run(self):
        """Starts the application."""
        self.view.show()
        sys.exit(self.app.exec())
