from game.piece import *  # كل حركات القطع
from game.move import Move  # كلاس الحركة
import copy  # علشان نعمل نسخة من البورد

# ================== VALID MOVES ==================
def get_valid_moves(board, row, col):
    piece = board[row][col]  # بنجيب القطعة

    if piece == "":
        return []  # مفيش قطعة

    # -------- Pawn --------
    if piece in ["wp", "bp"]:
        return pawn_moves(board, row, col)

    # -------- Rook --------
    elif piece in ["wr", "br"]:
        return rook_moves(board, row, col)

    # -------- Knight --------
    elif piece in ["wn", "bn"]:
        return knight_moves(board, row, col)

    # -------- Bishop --------
    elif piece in ["wb", "bb"]:
        return bishop_moves(board, row, col)

    # -------- Queen --------
    elif piece in ["wq", "bq"]:
        return queen_moves(board, row, col)

    # -------- King --------
    elif piece in ["wk", "bk"]:
        return king_moves(board, row, col)  # بدون فلترة check

    return []


# ================== LEGAL MOVES ==================
def get_legal_moves(board_obj, color):
    board = board_obj.board
    moves = []

    for r in range(8):
        for c in range(8):
            piece = board[r][c]

            if piece != "" and piece[0] == color:
                valid = get_valid_moves(board, r, c)

                for (r2, c2) in valid:
                    move = Move((r, c), (r2, c2))

                    # نجرب الحركة
                    new_board = copy.deepcopy(board_obj)
                    new_board.move_piece(move)

                    # لو الملك مش في check بعد الحركة
                    if not is_in_check(new_board, color):
                        moves.append(move)

    return moves


# ================== CHECK ==================
def is_in_check(board_obj, color):
    board = board_obj.board

    # نلاقي مكان الملك
    king_pos = None

    for r in range(8):
        for c in range(8):
            if board[r][c] == color + "k":
                king_pos = (r, c)
                break

    # لون العدو
    enemy = "b" if color == "w" else "w"

    # نشوف هل حد يقدر يضرب الملك
    for r in range(8):
        for c in range(8):
            piece = board[r][c]

            if piece != "" and piece[0] == enemy:
                moves = get_valid_moves(board, r, c)

                if king_pos in moves:
                    return True

    return False


# ================== CHECKMATE ==================
def is_checkmate(board_obj, color):
    if not is_in_check(board_obj, color):
        return False

    moves = get_legal_moves(board_obj, color)

    if len(moves) > 0:
        return False

    return True


# ================== STALEMATE ==================
def is_stalemate(board_obj, color):
    if is_in_check(board_obj, color):
        return False

    moves = get_legal_moves(board_obj, color)

    if len(moves) > 0:
        return False

    return True