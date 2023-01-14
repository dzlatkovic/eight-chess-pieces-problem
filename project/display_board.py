def display_board(position):
    notation_to_col = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7
    }
    board = [['.' for c in range(8)]
             for r in range(8)]
    """
    8x8 matrix is created
    """
    coordinates = position.split()
    for pos in coordinates:
        piece, coord = pos[0], pos[1:]
        row, col = 8 - int(coord[1]), notation_to_col[coord[0]]
        board[row][col] = piece

    for row in board:
        print(' '.join(row))


if __name__ == "__main__":
    """
    Copy-paste a row from the output:
    space-separated algebraic coordinates.
    e.g. Qc2: Piece symbol, then file (column) and
    finally rank (row). 
    """
    display_board("Bd4 Bd5 Kb4 Nd6 Nd7 Qc2 Re1 Rg3")
