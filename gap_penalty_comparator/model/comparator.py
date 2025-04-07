import blosum as bl
import numpy as np


def needleman_wunsch(s1, s2, gap_penalty, use_blosum):
    """
    Implement the Needleman-Wunsch algorithm for global alignment.

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
    arrow_matrix = np.zeros(value_matrix.shape, dtype=object)

    if use_blosum:
        blosum_matrix = bl.BLOSUM(62)

    for row_idx in range(1, value_matrix.shape[0]):
        for col_idx in range(1, value_matrix.shape[1]):
            is_match = s1[row_idx - 1] == s2[col_idx - 1]

            top_val = value_matrix[row_idx - 1, col_idx] + gap_penalty
            left_val = value_matrix[row_idx, col_idx - 1] + gap_penalty

            if use_blosum:
                diag_val = value_matrix[row_idx - 1, col_idx - 1] + blosum_matrix[s1[row_idx - 1]][s2[col_idx - 1]]
            else:
                diag_val = value_matrix[row_idx - 1, col_idx - 1] + (match_score if is_match else mismatch_score)

            value_matrix[row_idx, col_idx] = max(top_val, left_val, diag_val)
            arrow_matrix[row_idx, col_idx] = value_to_arrows(top_val, left_val, diag_val)

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

    row_idx = len(s1)
    col_idx = len(s2)
    coordinates.append((row_idx, col_idx))

    while row_idx > 0 and col_idx > 0:
        prev_cell_arrows = arrow_matrix[row_idx, col_idx]

        if len(prev_cell_arrows) > 1:
            # If there are multiple arrows, choose the one leading to the highest value
            top_val = value_matrix[row_idx - 1, col_idx]
            left_val = value_matrix[row_idx, col_idx - 1]
            diag_val = value_matrix[row_idx - 1, col_idx - 1]
            
            if 1 in prev_cell_arrows and diag_val >= top_val and diag_val >= left_val:
                row_idx -= 1
                col_idx -= 1
            elif 2 in prev_cell_arrows and top_val >= diag_val and top_val >= left_val:
                row_idx -= 1
            elif 3 in prev_cell_arrows and left_val >= diag_val and left_val >= top_val:
                col_idx -= 1

        elif 1 in prev_cell_arrows:
            row_idx -= 1
            col_idx -= 1
        elif 2 in prev_cell_arrows:
            row_idx -= 1
        elif 3 in prev_cell_arrows:
            col_idx -= 1

        coordinates.append((row_idx, col_idx))

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
        row_idx, col_idx = coordinates[i]
        next_row_idx, next_col_idx = coordinates[i + 1]
        same_row = row_idx == next_row_idx
        same_col = col_idx == next_col_idx

        if (same_row and col_idx != next_col_idx) or (same_col and row_idx != next_row_idx):
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
