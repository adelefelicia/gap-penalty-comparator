import blosum as bl
import numpy as np


def value_propagation(s1, s2, gap_penalty, use_blosum):
    """
    Constructs the alignment matrix according to the Needleman-Wunsch algorithm
    for global alignment.

    Args:
        s1 (str): sequence 1
        s2 (str): sequence 2
        gap_penalty (int): penalty for gaps
        use_blosum (bool): whether to use BLOSUM62 matrix for scoring (True), or
                            match/mismatch scoring of 1/-1 (False)

    Returns:
        (tuple): tuple containing:
        value_matrix (np.array): The alignment matrix with scores
        arrow_matrix (np.array): The matrix with values representing arrows for backtracking.
                                1 for diagonal, 2 for top, 3 for left
    """
    match_score = 1
    mismatch_score = -1

    value_matrix = initialize_value_matrix(s1, s2, gap_penalty)
    arrow_matrix = initialize_arrow_matrix(s1, s2)

    if use_blosum:
        blosum_matrix = bl.BLOSUM(62)

    for row in range(1, value_matrix.shape[0]):
        for col in range(1, value_matrix.shape[1]):
            s1_char = s1[row - 1]
            s2_char = s2[col - 1]

            is_match = s1_char == s2_char

            top_val = value_matrix[row - 1, col] + gap_penalty
            left_val = value_matrix[row, col - 1] + gap_penalty

            if use_blosum:
                diag_val = value_matrix[row - 1, col - 1] + blosum_matrix[s1_char][s2_char]
            else:
                diag_val = value_matrix[row - 1, col - 1] + (match_score if is_match else mismatch_score)

            value_matrix[row, col] = max(top_val, left_val, diag_val)
            arrow_matrix[row, col] = value_to_arrows(top_val, left_val, diag_val)

    return value_matrix, arrow_matrix

def value_to_arrows(top_val, left_val, diag_val):
    """
    Find corresponding arrows for backtracking.
    Represented by 1 for diagonal, 2 for top, 3 for left.
    """
    arrows = []
    if diag_val >= top_val and diag_val >= left_val:
        arrows.append(1)
    if top_val >= diag_val and top_val >= left_val:
        arrows.append(2)
    if left_val >= diag_val and left_val >= top_val:
        arrows.append(3)
    
    return np.array(arrows)

def initialize_arrow_matrix(s1, s2):
    """
    Initialize the arrow matrix with the correct dimensions and values.
    No arrows for position (0,0), [3] for the first row, and [2] for the first column.
    """
    matrix = np.zeros((len(s1) + 1, len(s2) + 1), dtype=object)
    for col in range(1, matrix.shape[1]):
        matrix[0, col] = [3]
    for row in range(1, matrix.shape[0]):
        matrix[row, 0] = [2]

    matrix[0, 0] = []
    return matrix

def initialize_value_matrix(s1, s2, gap_penalty):
    """
    Initialize the matrix with the correct dimensions and values.
    0 for position (0,0), and gap penalties incrementally for the
    first row and column.
    """
    matrix = np.zeros((len(s1) + 1, len(s2) + 1))

    if gap_penalty != 0:
        matrix[0, :] = np.arange(0, (len(s2) + 1) * gap_penalty, gap_penalty)
        matrix[:, 0] = np.arange(0, (len(s1) + 1) * gap_penalty, gap_penalty)

    return matrix

def backtrack_global_alignment(s1, s2, arrow_matrix, value_matrix):
    coordinates = []

    row = len(s1)
    col = len(s2)
    coordinates.append((row, col))

    while not (row == 0 and col == 0):
        prev_cell_arrows = arrow_matrix[row, col]

        if len(prev_cell_arrows) > 1:
            # If there are multiple arrows, choose the one leading to the highest value
            top_val = value_matrix[row - 1, col]
            left_val = value_matrix[row, col - 1]
            diag_val = value_matrix[row - 1, col - 1]
            
            if 1 in prev_cell_arrows and diag_val >= top_val and diag_val >= left_val:
                row -= 1
                col -= 1
            elif 2 in prev_cell_arrows and top_val >= diag_val and top_val >= left_val:
                row -= 1
            elif 3 in prev_cell_arrows and left_val >= diag_val and left_val >= top_val:
                col -= 1

        elif 1 in prev_cell_arrows:
            row -= 1
            col -= 1
        elif 2 in prev_cell_arrows:
            row -= 1
        elif 3 in prev_cell_arrows:
            col -= 1

        coordinates.append((row, col))

    return coordinates

def find_gaps(coordinates):
    """
    Find the number of gaps in the alignment.
    Returns:
        gaps (list): list of lengths of gaps found in the alignment
    """
    gaps = []
    prev_gap = {"count": 0, "seq": 0}
    for i in range(len(coordinates) - 1):
        row, col = coordinates[i]
        next_row, next_col = coordinates[i + 1]
        same_row = row == next_row
        same_col = col == next_col

        if (same_row and col != next_col) or (same_col and row != next_row):
            # Check if the gap is extending the previous one, or start a new one
            prev_gap = extends_prev_gap(prev_gap, same_row, same_col, gaps)

        # If there is no gap, assume any previous is closed
        elif prev_gap["count"] > 0:
            prev_gap, gaps = close_gap(prev_gap, gaps)

    return gaps

def extends_prev_gap(prev_gap, same_row, same_col, gaps):
    """
    Check if the current gap extends the previous one, otherwise start a new gap.
    """
    # Check if the gap is extending the previous one
    if prev_gap["seq"] == 1 and same_row:
        prev_gap["count"] += 1
    elif prev_gap["seq"] == 2 and same_col:
        prev_gap["count"] += 1
    # If the gap alternates between sequences, close the previous gap and start a new one
    elif (prev_gap["seq"] == 1 and same_col) or (prev_gap["seq"] == 2 and same_row):
        prev_gap, gaps = close_gap(prev_gap, gaps)
        prev_gap["count"] = 1
        prev_gap["seq"] = 1 if same_row else 2
    # Start a new gap if no previous gap exists
    elif prev_gap["seq"] == 0:
        prev_gap["count"] = 1
        prev_gap["seq"] = 1 if same_row else 2

    return prev_gap

def close_gap(prev_gap, gaps):
    """
    Close the previous gap by adding count to list of gaps and
    setting counter and seq to 0."""
    gaps.append(prev_gap["count"])
    prev_gap["count"] = 0
    prev_gap["seq"] = 0
    
    return prev_gap, gaps
