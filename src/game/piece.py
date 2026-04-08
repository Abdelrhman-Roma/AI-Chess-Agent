def in_bounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8


# ================= PAWN =================
def pawn_moves(board_obj, r, c):
    board = board_obj.board
    piece = board[r][c]
    moves = []

    direction = -1 if piece[0] == "w" else 1
    enemy = "b" if piece[0] == "w" else "w"
    one_step_row = r + direction

    # move forward
    if in_bounds(one_step_row, c) and board[one_step_row][c] == "":
        moves.append((one_step_row, c))

        start_row = 6 if piece[0] == "w" else 1
        two_step_row = r + 2 * direction
        if r == start_row and in_bounds(two_step_row, c) and board[two_step_row][c] == "":
            moves.append((two_step_row, c))

    # captures
    for dc in (-1, 1):
        nr, nc = r + direction, c + dc
        if in_bounds(nr, nc) and board[nr][nc] != "" and board[nr][nc][0] == enemy:
            moves.append((nr, nc))

    # en passant
    if board_obj.en_passant_target:
        target_r, target_c = board_obj.en_passant_target
        if target_r == r + direction and abs(target_c - c) == 1:
            adjacent_piece = board[r][target_c]
            if adjacent_piece == enemy + "p":
                moves.append((target_r, target_c))

    return moves


# ================= PAWN ATTACKS =================
def pawn_attacks(board_obj, r, c):
    board = board_obj.board
    piece = board[r][c]
    moves = []

    direction = -1 if piece[0] == "w" else 1

    for dc in (-1, 1):
        nr, nc = r + direction, c + dc
        if in_bounds(nr, nc):
            moves.append((nr, nc))

    return moves


# ================= ROOK =================
def rook_moves(board, r, c):
    moves = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for dr, dc in directions:
        for i in range(1, 8):
            nr, nc = r + dr * i, c + dc * i
            if not in_bounds(nr, nc):
                break

            if board[nr][nc] == "":
                moves.append((nr, nc))
            else:
                if board[nr][nc][0] != board[r][c][0]:
                    moves.append((nr, nc))
                break

    return moves


# ================= KNIGHT =================
def knight_moves(board, r, c):
    moves = []
    steps = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2),
    ]

    for dr, dc in steps:
        nr, nc = r + dr, c + dc
        if in_bounds(nr, nc):
            if board[nr][nc] == "" or board[nr][nc][0] != board[r][c][0]:
                moves.append((nr, nc))

    return moves


# ================= BISHOP =================
def bishop_moves(board, r, c):
    moves = []
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    for dr, dc in directions:
        for i in range(1, 8):
            nr, nc = r + dr * i, c + dc * i
            if not in_bounds(nr, nc):
                break

            if board[nr][nc] == "":
                moves.append((nr, nc))
            else:
                if board[nr][nc][0] != board[r][c][0]:
                    moves.append((nr, nc))
                break

    return moves


# ================= QUEEN =================
def queen_moves(board, r, c):
    return rook_moves(board, r, c) + bishop_moves(board, r, c)


# ================= KING ATTACKS =================
def king_attacks(r, c):
    moves = []

    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue

            nr, nc = r + dr, c + dc
            if in_bounds(nr, nc):
                moves.append((nr, nc))

    return moves


# ================= KING =================
def king_moves(board_obj, r, c):
    board = board_obj.board
    piece = board[r][c]
    moves = []

    for nr, nc in king_attacks(r, c):
        if board[nr][nc] == "" or board[nr][nc][0] != piece[0]:
            moves.append((nr, nc))

    color = piece[0]

    # castling availability is checked more deeply in rules.py
    if color == "w":
        if board_obj.can_castle_kingside("w"):
            moves.append((7, 6))
        if board_obj.can_castle_queenside("w"):
            moves.append((7, 2))
    else:
        if board_obj.can_castle_kingside("b"):
            moves.append((0, 6))
        if board_obj.can_castle_queenside("b"):
            moves.append((0, 2))

    return moves
