# ================= PAWN =================
def pawn_moves(board_obj, r, c):
    board = board_obj.board
    piece = board[r][c]
    moves = []

    direction = -1 if piece[0] == "w" else 1
    enemy = "b" if piece[0] == "w" else "w"

    # خطوة قدام
    if 0 <= r + direction < 8:
        if board[r + direction][c] == "":
            moves.append((r + direction, c))

            # أول مرة خطوتين
            if (r == 6 and piece[0] == "w") or (r == 1 and piece[0] == "b"):
                if board[r + 2 * direction][c] == "":
                    moves.append((r + 2 * direction, c))

    # ضرب قطري
    for dc in [-1, 1]:
        nr, nc = r + direction, c + dc
        if 0 <= nr < 8 and 0 <= nc < 8:
            if board[nr][nc] != "" and board[nr][nc][0] == enemy:
                moves.append((nr, nc))

    # ================= EN PASSANT =================
    if board_obj.en_passant_target:
        if (r + direction, c - 1) == board_obj.en_passant_target:
            moves.append(board_obj.en_passant_target)
        if (r + direction, c + 1) == board_obj.en_passant_target:
            moves.append(board_obj.en_passant_target)

    return moves


# ================= ROOK =================
def rook_moves(board, r, c):
    moves = []
    directions = [(1,0),(-1,0),(0,1),(0,-1)]

    for dr, dc in directions:
        for i in range(1, 8):
            nr, nc = r + dr*i, c + dc*i
            if 0 <= nr < 8 and 0 <= nc < 8:
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
    steps = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]

    for dr, dc in steps:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 8 and 0 <= nc < 8:
            if board[nr][nc] == "" or board[nr][nc][0] != board[r][c][0]:
                moves.append((nr, nc))
    return moves


# ================= BISHOP =================
def bishop_moves(board, r, c):
    moves = []
    directions = [(1,1),(1,-1),(-1,1),(-1,-1)]

    for dr, dc in directions:
        for i in range(1, 8):
            nr, nc = r + dr*i, c + dc*i
            if 0 <= nr < 8 and 0 <= nc < 8:
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


# ================= KING =================
def king_moves(board_obj, r, c):
    board = board_obj.board
    moves = []

    # الحركات العادية
    for dr in [-1,0,1]:
        for dc in [-1,0,1]:
            if dr == 0 and dc == 0:
                continue

            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if board[nr][nc] == "" or board[nr][nc][0] != board[r][c][0]:
                    moves.append((nr, nc))

    # ================= CASTLING =================
    piece = board[r][c]

    # White
    if piece == "wk" and not board_obj.white_king_moved:

        # King side
        if board[7][5] == "" and board[7][6] == "":
            if board[7][7] == "wr":
                moves.append((7, 6))

        # Queen side
        if board[7][1] == "" and board[7][2] == "" and board[7][3] == "":
            if board[7][0] == "wr":
                moves.append((7, 2))

    # Black
    if piece == "bk" and not board_obj.black_king_moved:

        # King side
        if board[0][5] == "" and board[0][6] == "":
            if board[0][7] == "br":
                moves.append((0, 6))

        # Queen side
        if board[0][1] == "" and board[0][2] == "" and board[0][3] == "":
            if board[0][0] == "br":
                moves.append((0, 2))

    return moves