# ============================================
# Heuristic 1: Basic Material (300-500 ELO)
# ============================================
def heuristics_1(board_obj):
    values = {
        "p": 100,
        "n": 320,
        "b": 330,
        "r": 500,
        "q": 900,
        "k": 0,
    }

    score = 0

    for row in board_obj.board:
        for piece in row:
            if piece:
                val = values[piece[1]]
                score += val if piece[0] == "w" else -val

    return score


# ============================================
# Heuristic 2: Material + Position (600-1000 ELO)
# ============================================
def heuristics_2(board_obj):
    board = board_obj.board

    values = {
        "p": 100,
        "n": 320,
        "b": 330,
        "r": 500,
        "q": 900,
        "k": 0,
    }

    pawn_table = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]

    knight_table = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50],
    ]

    bishop_table = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20],
    ]

    tables = {
        "p": pawn_table,
        "n": knight_table,
        "b": bishop_table,
    }

    score = 0

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if not piece:
                continue

            color = piece[0]
            ptype = piece[1]

            val = values[ptype]
            score += val if color == "w" else -val

            if ptype in tables:
                table_row = 7 - r if color == "w" else r
                positional_score = tables[ptype][table_row][c]
                score += positional_score if color == "w" else -positional_score

    return score


# ============================================
# Heuristic 3: Advanced (1000-1500 ELO)
# ============================================
def heuristics_3(board_obj):
    board = board_obj.board

    values = {
        "p": 100,
        "n": 320,
        "b": 330,
        "r": 500,
        "q": 900,
        "k": 0,
    }

    center_squares = {(3, 3), (3, 4), (4, 3), (4, 4)}

    material = 0
    center = 0
    bishop_pair = {"w": 0, "b": 0}
    pawn_penalty = 0

    white_pawns_by_file = [0] * 8
    black_pawns_by_file = [0] * 8

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if not piece:
                continue

            color = piece[0]
            ptype = piece[1]

            val = values[ptype]
            material += val if color == "w" else -val

            if (r, c) in center_squares:
                center += 20 if color == "w" else -20

            if ptype == "b":
                bishop_pair[color] += 1

            if ptype == "p":
                if color == "w":
                    white_pawns_by_file[c] += 1
                else:
                    black_pawns_by_file[c] += 1

    for count in white_pawns_by_file:
        if count > 1:
            pawn_penalty -= 10 * (count - 1)

    for count in black_pawns_by_file:
        if count > 1:
            pawn_penalty += 10 * (count - 1)

    bishop_score = 0
    if bishop_pair["w"] >= 2:
        bishop_score += 30
    if bishop_pair["b"] >= 2:
        bishop_score -= 30

    return material + center + bishop_score + pawn_penalty
