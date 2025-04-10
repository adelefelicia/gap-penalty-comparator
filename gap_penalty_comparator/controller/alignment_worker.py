from model.needleman_wunsch import (backtrack_global_alignment, find_gaps,
                                    value_propagation)
from PyQt6.QtCore import QThread, pyqtSignal


class AlignmentWorker(QThread):
    result_ready = pyqtSignal(list, list, list, list)  # Signal to send results back to the main thread
    error_occurred = pyqtSignal(str)  # Signal to send error messages

    def __init__(self, seq1, seq2, gap_penalties, scoring_method):
        super().__init__()
        self.seq1 = seq1
        self.seq2 = seq2
        self.gap_penalties = gap_penalties
        self.scoring_method = scoring_method

    def run(self):
        try:
            value_matrices = []
            arrow_matrices = []
            alignment_coordinates = []
            gaps = []

            for penalty in self.gap_penalties:
                val_matrix, arrow_matrix = value_propagation(self.seq1, self.seq2, penalty, self.scoring_method == "BLOSUM62")
                coordinate_list = backtrack_global_alignment(self.seq1, self.seq2, arrow_matrix, val_matrix)

                value_matrices.append(val_matrix)
                arrow_matrices.append(arrow_matrix)
                alignment_coordinates.append(coordinate_list)
                gaps.append(find_gaps(coordinate_list))

            self.result_ready.emit(value_matrices, arrow_matrices, alignment_coordinates, gaps)
        except Exception as e:
            self.error_occurred.emit(str(e))