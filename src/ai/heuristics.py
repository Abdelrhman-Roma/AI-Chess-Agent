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
        "k": 0
    }

    score = 0
    board = board_obj.board

    for row in board:
        for piece in row:
            if piece:
                val = values[piece[1]]
                score += val if piece[0] == "w" else -val

    return score


# ============================================
# Heuristic 2: Material + Position + Mobility
# (600 - 1000 ELO)
# ============================================
def heuristics_2(board_obj):
    board = board_obj.board

    # Piece values
    values = {
        "p": 100,
        "n": 320,
        "b": 330,
        "r": 500,
        "q": 900,
        "k": 0
    }

    # Pawn table
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
    mobility = 0

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if not piece:
                continue

            color = piece[0]
            ptype = piece[1]

            # Material
            val = values[ptype]
            score += val if color == "w" else -val

            # Position
            if ptype in tables:
                if color == "w":
                    score += tables[ptype][r][c]
                else:
                    score -= tables[ptype][7-r][c]

            # Mobility (عدد الحركات التقريبي)
            if ptype in ["n", "b", "r", "q"]:
                mobility += 1 if color == "w" else -1

    return score + mobility * 5


# ============================================
# Heuristic 3: Advanced Evaluation
# (1000 - 1500 ELO)
# ============================================
def heuristics_3(board_obj):
    board = board_obj.board

    values = {
        'p': 100,
        'n': 320,
        'b': 330,
        'r': 500,
        'q': 900,
        'k': 20000
    }

    center_squares = [(3,3),(3,4),(4,3),(4,4)]

    material = 0
    center = 0
    bishop_pair = {"w":0,"b":0}
    pawn_structure = 0
    king_safety = 0

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if not piece:
                continue

            color = piece[0]
            ptype = piece[1]

            val = values[ptype]

            # Material
            material += val if color == "w" else -val

            # Center control
            if (r, c) in center_squares:
                center += 20 if color == "w" else -20

            # Bishop pair
            if ptype == "b":
                bishop_pair[color] += 1

            # Pawn structure (penalty for doubled pawns)
            if ptype == "p":
                for rr in range(8):
                    if rr != r and board[rr][c] == piece:
                        pawn_structure -= 10 if color == "w" else -10

            # King safety (very simple)
            if ptype == "k":
                if color == "w":
                    king_safety -= abs(7 - r) * 5
                else:
                    king_safety += abs(0 - r) * 5

    bishop_score = 0
    if bishop_pair["w"] >= 2:
        bishop_score += 30
    if bishop_pair["b"] >= 2:
        bishop_score -= 30

    return material + center + bishop_score + pawn_structure + king_safety