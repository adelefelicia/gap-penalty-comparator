import sys

from PyQt6.QtWidgets import QApplication, QPushButton
from view.app import MainWindow

from .alignment_worker import AlignmentWorker


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
            scoring_method = self.view.get_scoring_method()

            if not seq1 or not seq2:
                self.view.popup_dialog("Please enter both sequences.", "warning")
                return
            
            if not self.validate_seq_input(seq1, seq2):
                self.view.popup_dialog("One or both sequences contain invalid characters. Only letters representing amino acids and nucleotides are allowed.", "warning")
                return

            if len(seq1) > 30 or len(seq2) > 30:
                self.view.popup_dialog("Matrices for sequences over 30 characters may be hard to read.", "info")

            gap_penalties = self.view.get_gap_penalties()

            if len(gap_penalties) < 3:
                self.view.popup_dialog("Please enter three gap penalties to compare.", "warning")
                return

            self.view.loading_cursor(True)

            # Create and start the worker thread to run the algorithm in parallell with the GUI's main thread
            self.worker = AlignmentWorker(seq1, seq2, gap_penalties, scoring_method)
            self.worker.result_ready.connect(self.on_results_ready)
            self.worker.error_occurred.connect(self.on_error)
            self.worker.finished.connect(lambda: self.view.loading_cursor(False))
            self.worker.start()

        except Exception as e:
            print(e)
            self.view.popup_dialog(f"An unexpected error occurred. Try restarting the application.", "error")
    
    def on_results_ready(self, value_matrices, arrow_matrices, alignment_coordinates, gaps):
        """Handle results from the worker thread."""
        self.view.set_gaps(gaps)
        self.view.display_matrices(value_matrices, arrow_matrices, (self.worker.seq1, self.worker.seq2), alignment_coordinates, self.worker.gap_penalties)
        self.view.loading_cursor(False)

    def on_error(self, error_message):
        """Handle errors from the worker thread."""
        raise Exception(f"An error occured during the algorithm execution: {error_message}")

    def parse_input(self, input1, input2):
        """
        Parse the input strings by removing whitespace and converting
        them to uppercase.
        """
        input1 = ''.join(input1.upper().split())
        input2 = ''.join(input2.upper().split())

        return input1, input2

    def validate_seq_input(self, input1, input2):
        """
        Validate the input sequences to ensure they only contain valid
        amino acid / nucleotide characters.
        """
        valid_chars = set("ARNDCQEGHILKMFPSTWYVBZX")
        if set(input1).issubset(valid_chars) and set(input2).issubset(valid_chars):
            return True
        else:
            return False

    def run(self):
        """Starts the application."""
        self.view.show()
        sys.exit(self.app.exec())
