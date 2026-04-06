# ============================================
# Heuristic 1: Basic Material
# ============================================
def heuristics_1(board_obj):
    values = {
        "p": 100,
        "n": 320,
        "b": 330,
        "r": 500,
        "q": 900,
        "k": 0
    }

    score = 0

    for row in board_obj.board:
        for piece in row:
            if piece != "":
                value = values[piece[1]]

                if piece[0] == "w":
                    score += value
                else:
                    score -= value

    return score


# ============================================
# Heuristic 2: Position + Tables (بتاعتك)
# ============================================
def heuristics_2(board_obj):
    board = board_obj.board

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

    tables = {
        "p": PAWN_TABLE,
        "n": KNIGHT_TABLE
    }

    score = 0

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece == "":
                continue

            color = piece[0]
            ptype = piece[1]

            if ptype in tables:
                if color == "w":
                    score += tables[ptype][r][c]
                else:
                    score -= tables[ptype][7-r][c]

    return heuristics_1(board_obj) + score


# ============================================
# Heuristic 3: Advanced (FIXED)
# ============================================
def heuristics_3(board_obj):
    board = board_obj.board

    values = {
        'p': 100,
        'n': 320,
        'b': 330,
        'r': 500,
        'q': 900,
        'k': 0
    }

    center_squares = [(3,3),(3,4),(4,3),(4,4)]

    material = 0
    center = 0
    bishop_pair = {"w":0,"b":0}

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece == "":
                continue

            color = piece[0]
            ptype = piece[1]

            val = values[ptype]

            # Material
            if color == "w":
                material += val
            else:
                material -= val

            # Center
            if (r,c) in center_squares:
                if color == "w":
                    center += 10
                else:
                    center -= 10

            # Bishop pair
            if ptype == "b":
                bishop_pair[color] += 1

    # Bishop bonus
    bishop_score = 0
    if bishop_pair["w"] >= 2:
        bishop_score += 30
    if bishop_pair["b"] >= 2:
        bishop_score -= 30

    return material + center + bishop_score