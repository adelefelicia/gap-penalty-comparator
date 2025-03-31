import sys
from PyQt6.QtWidgets import QApplication, QPushButton
from view.main_view import MainView
from model.comparator import needleman_wunsch, backtrack_global_alignment
from view.matrices_view import MatricesView

class Controller:
    def __init__(self):
        self.app = QApplication([])
        self.main_view = MainView(self)
        self.matrices_view = MatricesView(self)

        # self.view.findChild(QPushButton, "submitBtn").clicked.connect(self.run_algorithm)

    def show_main_view(self):
        self.matrices_view.hide()
        self.main_view.show()

    def show_matrices_view(self):
        self.run_algorithm()
        self.main_view.hide()
        self.matrices_view.show()

    def run_algorithm(self):
        """Fetches inputs from the view, runs the algorithm, and updates the view with results."""
        seq1, seq2 = self.main_view.get_sequences() # TODO parse sequences
        gap_penalties = self.main_view.get_gap_penalties()

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

        self.matrices_view.display_matrices(value_matrices, arrow_matrices, (seq1, seq2), alignment_coordinates)

    def run(self):
        """Starts the application."""
        self.main_view.show()
        sys.exit(self.app.exec())
