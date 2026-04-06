from game.piece import pawn_moves, rook_moves, knight_moves, bishop_moves, queen_moves, king_moves
from game.move import Move
import copy


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


# ================== CHECK ==================
def is_in_check(board_obj, color):
    board = board_obj.board
    king_pos = None

    # نلاقي مكان الملك
    for r in range(8):
        for c in range(8):
            if board[r][c] == color + "k":
                king_pos = (r, c)
                break

    enemy = "b" if color == "w" else "w"

    # نشوف هل الملك تحت تهديد
    for r in range(8):
        for c in range(8):
            piece = board[r][c]

            if piece != "" and piece[0] == enemy:
                moves = get_valid_moves(board_obj, r, c)

                if king_pos in moves:
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

                for (r2, c2) in valid_moves:
                    move = Move((r, c), (r2, c2))

                    # نعمل نسخة من البورد
                    new_board = copy.deepcopy(board_obj)
                    new_board.make_move(move)

                    # نتأكد إن الملك مش في check
                    if not is_in_check(new_board, color):
                        moves.append(move)

    return moves


# ================== CHECKMATE ==================
def is_checkmate(board_obj, color):
    # لو مش في check يبقى مش checkmate
    if not is_in_check(board_obj, color):
        return False

    # لو مفيش أي moves قانونية يبقى مات
    moves = get_legal_moves(board_obj, color)
    return len(moves) == 0


# ================== STALEMATE ==================
def is_stalemate(board_obj, color):
    # لو في check يبقى مش stalemate
    if is_in_check(board_obj, color):
        return False

    # لو مفيش moves يبقى تعادل
    moves = get_legal_moves(board_obj, color)
    return len(moves) == 0