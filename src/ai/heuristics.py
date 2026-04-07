# ============================================
# Heuristic 1: Basic Material (300-500 ELO)
# ============================================
def heuristics_1(board_obj):
    values = {
        "p": 100, "n": 320, "b": 330,
        "r": 500, "q": 900, "k": 0
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
        "p": 100, "n": 320, "b": 330,
        "r": 500, "q": 900, "k": 0
    }

    PAWN_TABLE = [
        [0,0,0,0,0,0,0,0],
        [50,50,50,50,50,50,50,50],
        [10,10,20,30,30,20,10,10],
        [5,5,10,25,25,10,5,5],
        [0,0,0,20,20,0,0,0],
        [5,-5,-10,0,0,-10,-5,5],
        [5,10,10,-20,-20,10,10,5],
        [0,0,0,0,0,0,0,0]
    ]

    KNIGHT_TABLE = [
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,0,0,0,0,-20,-40],
        [-30,0,10,15,15,10,0,-30],
        [-30,5,15,20,20,15,5,-30],
        [-30,0,15,20,20,15,0,-30],
        [-30,5,10,15,15,10,5,-30],
        [-40,-20,0,5,5,0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
    ]

    BISHOP_TABLE = [
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,0,0,0,0,0,0,-10],
        [-10,0,5,10,10,5,0,-10],
        [-10,5,5,10,10,5,5,-10],
        [-10,0,10,10,10,10,0,-10],
        [-10,10,10,10,10,10,10,-10],
        [-10,5,0,0,0,0,5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ]

    tables = {
        "p": PAWN_TABLE,
        "n": KNIGHT_TABLE,
        "b": BISHOP_TABLE
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

            # material
            score += val if color == "w" else -val

            # position
            if ptype in tables:
                if color == "w":
                    score += tables[ptype][r][c]
                else:
                    score -= tables[ptype][7 - r][c]

    return score


# ============================================
# Heuristic 3: Advanced (1000-1500 ELO)
# ============================================
def heuristics_3(board_obj):
    board = board_obj.board

    values = {
        "p": 100, "n": 320, "b": 330,
        "r": 500, "q": 900, "k": 0
    }

    center_squares = [(3,3),(3,4),(4,3),(4,4)]

    material = 0
    center = 0
    bishop_pair = {"w": 0, "b": 0}
    pawn_penalty = 0

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if not piece:
                continue

            color = piece[0]
            ptype = piece[1]

            val = values[ptype]

            # material
            material += val if color == "w" else -val

            # center control
            if (r, c) in center_squares:
                center += 20 if color == "w" else -20

            # bishop pair
            if ptype == "b":
                bishop_pair[color] += 1

            # doubled pawn penalty
            if ptype == "p":
                for rr in range(8):
                    if rr != r and board[rr][c] == piece:
                        pawn_penalty -= 10 if color == "w" else -10

    bishop_score = 0
    if bishop_pair["w"] >= 2:
        bishop_score += 30
    if bishop_pair["b"] >= 2:
        bishop_score -= 30

    return material + center + bishop_score + pawn_penalty