import numpy as np


def needleman_wunsch(s1, s2, gap_penalty=-2):
    """
    Implement the Needleman-Wunsch algorithm for global alignment.

    Args:
        s1 (str): sequence 1
        s2 (str): sequence 2
        gap_penalty (int): penalty for gaps, default is -2

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

    for row_idx in range(1, value_matrix.shape[0]):
        for col_idx in range(1, value_matrix.shape[1]):
            is_match = s1[row_idx - 1] == s2[col_idx - 1]

            top_val = value_matrix[row_idx - 1, col_idx] + gap_penalty
            left_val = value_matrix[row_idx, col_idx - 1] + gap_penalty
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
            
            if diag_val >= top_val and diag_val >= left_val:
                row_idx -= 1
                col_idx -= 1
            elif top_val >= diag_val and top_val >= left_val:
                row_idx -= 1
            elif left_val >= diag_val and left_val >= top_val:
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
