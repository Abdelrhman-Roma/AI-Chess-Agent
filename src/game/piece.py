# ================== PAWN ==================
def pawn_moves(board, row, col):
    piece = board[row][col]
    moves = []

    # -------- White Pawn --------
    if piece == "wp":

        # خطوة قدام
        if row - 1 >= 0 and board[row - 1][col] == "":
            moves.append((row - 1, col))

            # خطوتين أول مرة
            if row == 6 and board[row - 2][col] == "":
                moves.append((row - 2, col))

        # أكل شمال
        if row - 1 >= 0 and col - 1 >= 0:
            if board[row - 1][col - 1] != "" and board[row - 1][col - 1][0] == "b":
                moves.append((row - 1, col - 1))

        # أكل يمين
        if row - 1 >= 0 and col + 1 < 8:
            if board[row - 1][col + 1] != "" and board[row - 1][col + 1][0] == "b":
                moves.append((row - 1, col + 1))

    # -------- Black Pawn --------
    elif piece == "bp":

        # خطوة قدام
        if row + 1 < 8 and board[row + 1][col] == "":
            moves.append((row + 1, col))

            # خطوتين أول مرة
            if row == 1 and board[row + 2][col] == "":
                moves.append((row + 2, col))

        # أكل شمال
        if row + 1 < 8 and col - 1 >= 0:
            if board[row + 1][col - 1] != "" and board[row + 1][col - 1][0] == "w":
                moves.append((row + 1, col - 1))

        # أكل يمين
        if row + 1 < 8 and col + 1 < 8:
            if board[row + 1][col + 1] != "" and board[row + 1][col + 1][0] == "w":
                moves.append((row + 1, col + 1))

    return moves


# ================== ROOK ==================
def rook_moves(board, row, col):
    piece = board[row][col]
    moves = []

    directions = [
        (-1, 0), (1, 0),  # فوق / تحت
        (0, -1), (0, 1)   # شمال / يمين
    ]

    for dr, dc in directions:
        r, c = row + dr, col + dc

        while 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == "":
                moves.append((r, c))
            else:
                if board[r][c][0] != piece[0]:
                    moves.append((r, c))
                break

            r += dr
            c += dc

    return moves


# ================== KNIGHT ==================
def knight_moves(board, row, col):
    piece = board[row][col]
    moves = []

    directions = [
        (-2, -1), (-2, 1),
        (-1, -2), (-1, 2),
        (1, -2),  (1, 2),
        (2, -1),  (2, 1)
    ]

    for dr, dc in directions:
        r = row + dr
        c = col + dc

        if 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == "" or board[r][c][0] != piece[0]:
                moves.append((r, c))

    return moves


# ================== BISHOP ==================
def bishop_moves(board, row, col):
    piece = board[row][col]
    moves = []

    directions = [
        (-1, -1), (-1, 1),
        (1, -1),  (1, 1)
    ]

    for dr, dc in directions:
        r, c = row + dr, col + dc

        while 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == "":
                moves.append((r, c))
            else:
                if board[r][c][0] != piece[0]:
                    moves.append((r, c))
                break

            r += dr
            c += dc

    return moves


# ================== QUEEN ==================
def queen_moves(board, row, col):
    return rook_moves(board, row, col) + bishop_moves(board, row, col)


# ================== KING ==================
def king_moves(board, row, col):
    piece = board[row][col]
    moves = []

    directions = [
        (-1, 0), (1, 0),   # فوق / تحت
        (0, -1), (0, 1),   # شمال / يمين
        (-1, -1), (-1, 1), # قطري فوق
        (1, -1),  (1, 1)   # قطري تحت
    ]

    for dr, dc in directions:
        r = row + dr
        c = col + dc

        if 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == "" or board[r][c][0] != piece[0]:
                moves.append((r, c))

    return moves