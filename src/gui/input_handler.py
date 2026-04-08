from game.rules import get_legal_moves


def handle_mouse_click(board_obj, selected_square, row, col, turn):
    board = board_obj.board

    if not (0 <= row < 8 and 0 <= col < 8):
        return selected_square

    # Select a piece
    if selected_square is None:
        if board[row][col] != "" and board[row][col][0] == turn:
            return (row, col)
        return None

    old_row, old_col = selected_square

    # Deselect the same square
    if (row, col) == selected_square:
        return None

    legal_moves = get_legal_moves(board_obj, turn)

    for move in legal_moves:
        if move.start == (old_row, old_col) and move.end == (row, col):
            board_obj.make_move(move)
            return None

    # Switch selection to another friendly piece
    if board[row][col] != "" and board[row][col][0] == turn:
        return (row, col)

    return selected_square
