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
        try:
            seq1, seq2 = self.view.get_sequences()
            seq1, seq2 = self.parse_input(seq1, seq2)

            if not seq1 or not seq2:
                self.view.popup_dialog("Please enter both sequences.", "warning")
                return

            if not seq1.isalpha() and seq2.isalpha():
                self.view.popup_dialog("One or both sequences contain invalid characters. Only letters are allowed.", "warning")
                return

            gap_penalties = self.view.get_gap_penalties()

            if len(gap_penalties) < 2:
                self.view.popup_dialog("Please enter at least two gap penalties to compare.", "warning")
                return

            value_matrices = []
            arrow_matrices = []
            alignment_coordinates = []

            for penalty in gap_penalties:
                val_matrix, arrow_matrix = needleman_wunsch(seq1, seq2, penalty)
                coordinate_list = backtrack_global_alignment(seq1, seq2, arrow_matrix)

                value_matrices.append(val_matrix)
                arrow_matrices.append(arrow_matrix)
                alignment_coordinates.append(coordinate_list)

            self.view.display_matrices(value_matrices, arrow_matrices, (seq1, seq2), alignment_coordinates, gap_penalties)

        except Exception as e:
            self.view.popup_dialog(f"An unexpected error occurred. Try restarting the application.", "error")

    def parse_input(self, input1, input2):
        """
        Parse the input strings by removing whitespace and converting
        them to uppercase.
        """
        input1 = ''.join(input1.upper().split())
        input2 = ''.join(input2.upper().split())

        return input1, input2

    def run(self):
        """Starts the application."""
        self.view.show()
        sys.exit(self.app.exec())
