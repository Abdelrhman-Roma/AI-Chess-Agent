# ============================================
# Heuristic 1: Easy - Material Only
# ============================================
def heuristics_1(board_obj):
    values = {
        "p": 100, "n": 320, "b": 330,
        "r": 500, "q": 900, "k": 0
    }
    score = 0
    for row in board_obj.board:
        for piece in row:
            if piece and piece != "":
                value = values.get(piece[1], 0)
                if piece[0] == "w":
                    score += value
                else:
                    score -= value
    return score


# ============================================
# Heuristic 2: Medium - Material + Position
# ============================================
def heuristics_2(board_obj):
    PAWN_TABLE = [
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [ 5,  5, 10, 25, 25, 10,  5,  5],
        [ 0,  0,  0, 20, 20,  0,  0,  0],
        [ 5, -5,-10,  0,  0,-10, -5,  5],
        [ 5, 10, 10,-20,-20, 10, 10,  5],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ]
    KNIGHT_TABLE = [
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
    ]
    BISHOP_TABLE = [
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ]
    ROOK_TABLE = [
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [ 0,  0,  0,  5,  5,  0,  0,  0]
    ]

    tables = {
        "p": PAWN_TABLE,
        "n": KNIGHT_TABLE,
        "b": BISHOP_TABLE,
        "r": ROOK_TABLE,
    }

    values = {
        "p": 100, "n": 320, "b": 330,
        "r": 500, "q": 900, "k": 0
    }

    score = 0
    board = board_obj.board

    # 🔥 loop واحدة بس بدل اتنين
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if not piece or piece == "":
                continue
            color = piece[0]
            ptype = piece[1]
            sign  = 1 if color == "w" else -1

            score += sign * values.get(ptype, 0)

            if ptype in tables:
                tval = tables[ptype][r][c] if color == "w" else tables[ptype][7 - r][c]
                score += sign * tval

    return score


# ============================================
# Heuristic 3: Hard - Material + Position + Strategy
# ============================================
def heuristics_3(board_obj):
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

    ROOK_TABLE = [
        [0,0,0,0,0,0,0,0],
        [5,10,10,10,10,10,10,5],
        [-5,0,0,0,0,0,0,-5],
        [-5,0,0,0,0,0,0,-5],
        [-5,0,0,0,0,0,0,-5],
        [-5,0,0,0,0,0,0,-5],
        [-5,0,0,0,0,0,0,-5],
        [0,0,0,5,5,0,0,0]
    ]

    QUEEN_TABLE = [
        [-20,-10,-10,-5,-5,-10,-10,-20],
        [-10,0,0,0,0,0,0,-10],
        [-10,0,5,5,5,5,0,-10],
        [-5,0,5,5,5,5,0,-5],
        [0,0,5,5,5,5,0,-5],
        [-10,5,5,5,5,5,0,-10],
        [-10,0,5,0,0,0,0,-10],
        [-20,-10,-10,-5,-5,-10,-10,-20]
    ]

    KING_TABLE = [
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [20,20,0,0,0,0,20,20],
        [20,30,10,0,0,10,30,20]
    ]

    tables = {
        "p": PAWN_TABLE, "n": KNIGHT_TABLE,
        "b": BISHOP_TABLE, "r": ROOK_TABLE,
        "q": QUEEN_TABLE, "k": KING_TABLE,
    }

    values = {
        "p": 100, "n": 320, "b": 330,
        "r": 500, "q": 900, "k": 0
    }

    score = 0
    bishop_count = {"w": 0, "b": 0}
    pawn_cols = {"w": {}, "b": {}}
    board = board_obj.board

    # 🔥 loop واحدة
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if not piece:
                continue

            color = piece[0]
            ptype = piece[1]
            sign = 1 if color == "w" else -1

            score += sign * values.get(ptype, 0)

            if ptype in tables:
                tval = tables[ptype][r][c] if color == "w" else tables[ptype][7 - r][c]
                score += sign * tval

            if ptype == "b":
                bishop_count[color] += 1

            if ptype == "p":
                pawn_cols[color][c] = pawn_cols[color].get(c, 0) + 1

    # isolated pawns
    for color, sign in [("w", 1), ("b", -1)]:
        cols = set(pawn_cols[color].keys())
        for col in cols:
            if not ({col - 1, col + 1} & cols):
                score -= sign * 15

    # doubled pawns (optimized)
    for color, sign in [("w", 1), ("b", -1)]:
        for col, count in pawn_cols[color].items():
            if count > 1:
                score -= sign * (count - 1) * 20

    # open files
    open_files = []
    for c in range(8):
        has_pawn = False
        for r in range(8):
            if board[r][c] and board[r][c][1] == "p":
                has_pawn = True
                break
        if not has_pawn:
            open_files.append(c)

    for r in range(8):
        for c in open_files:
            piece = board[r][c]
            if piece and piece[1] == "r":
                sign = 1 if piece[0] == "w" else -1
                score += sign * 20

    # bishop pair
    if bishop_count["w"] >= 2:
        score += 30
    if bishop_count["b"] >= 2:
        score -= 30

    # 🔥 NEW: mobility (بسيطة)
    try:
        score += len(board_obj.get_valid_moves("w")) * 5
        score -= len(board_obj.get_valid_moves("b")) * 5
    except:
        pass

    # 🔥 NEW: king safety بسيطة
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece[1] == "k":
                color = piece[0]
                sign = 1 if color == "w" else -1

                # لو حواليه بيادق = أمان
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 8 and 0 <= nc < 8:
                            p = board[nr][nc]
                            if p and p[1] == "p" and p[0] == color:
                                score += sign * 5

    return score
