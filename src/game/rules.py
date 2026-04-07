from game.piece import (
    pawn_moves,
    rook_moves,
    knight_moves,
    bishop_moves,
    queen_moves,
    king_moves,
    pawn_attacks
)
from game.move import Move


# ================== VALID MOVES ==================
def get_valid_moves(board_obj, row, col):
    board = board_obj.board
    piece = board[row][col]

    if piece == "":
        return []

    if piece[1] == "p":
        return pawn_moves(board_obj, row, col)

    elif piece[1] == "r":
        return rook_moves(board, row, col)

    elif piece[1] == "n":
        return knight_moves(board, row, col)

    elif piece[1] == "b":
        return bishop_moves(board, row, col)

    elif piece[1] == "q":
        return queen_moves(board, row, col)

    elif piece[1] == "k":
        return king_moves(board_obj, row, col)

    return []


# ================== ATTACK MOVES ==================
def get_attacks(board_obj, row, col):
    piece = board_obj.board[row][col]

    if piece == "":
        return []

    if piece[1] == "p":
        return pawn_attacks(board_obj, row, col)

    return get_valid_moves(board_obj, row, col)


# ================== FIND KING ==================
def find_king(board_obj, color):
    for r in range(8):
        for c in range(8):
            if board_obj.board[r][c] == color + "k":
                return (r, c)
    return None


# ================== CHECK ==================
def is_in_check(board_obj, color):
    king_pos = find_king(board_obj, color)

    if king_pos is None:
        return True

    enemy = "b" if color == "w" else "w"

    for r in range(8):
        for c in range(8):
            piece = board_obj.board[r][c]

            if piece != "" and piece[0] == enemy:
                attacks = get_attacks(board_obj, r, c)

                if king_pos in attacks:
                    return True

    return False


# ================== LEGAL MOVES ==================
def get_legal_moves(board_obj, color):
    moves = []

    for r in range(8):
        for c in range(8):
            piece = board_obj.board[r][c]

            if piece != "" and piece[0] == color:

                valid_moves = get_valid_moves(board_obj, r, c)

                # 🔥 أهم تعديل: فلترة حركات الملك
                if piece[1] == "k":
                    safe_moves = []

                    for (r2, c2) in valid_moves:
                        move = Move((r, c), (r2, c2))
                        board_obj.make_move(move)

                        if not is_in_check(board_obj, color):
                            safe_moves.append((r2, c2))

                        board_obj.undo_move()

                    valid_moves = safe_moves

                for (r2, c2) in valid_moves:

                    target = board_obj.board[r2][c2]

                    # منع أخذ الملك
                    if target != "" and target[1] == "k":
                        continue

                    move = Move((r, c), (r2, c2))

                    board_obj.make_move(move)

                    if not is_in_check(board_obj, color):
                        moves.append(move)

                    board_obj.undo_move()

    return moves


# ================== CHECKMATE ==================
def is_checkmate(board_obj, color):
    return is_in_check(board_obj, color) and len(get_legal_moves(board_obj, color)) == 0


# ================== STALEMATE ==================
def is_stalemate(board_obj, color):
    return not is_in_check(board_obj, color) and len(get_legal_moves(board_obj, color)) == 0