from game.piece import (
    pawn_moves,
    rook_moves,
    knight_moves,
    bishop_moves,
    queen_moves,
    king_moves,
    pawn_attacks,
    king_attacks,
)
from game.move import Move


# ================== VALID MOVES ==================
def get_valid_moves(board_obj, row, col):
    board = board_obj.board
    piece = board[row][col]

    if piece == "":
        return []

    piece_type = piece[1]

    if piece_type == "p":
        return pawn_moves(board_obj, row, col)
    if piece_type == "r":
        return rook_moves(board, row, col)
    if piece_type == "n":
        return knight_moves(board, row, col)
    if piece_type == "b":
        return bishop_moves(board, row, col)
    if piece_type == "q":
        return queen_moves(board, row, col)
    if piece_type == "k":
        return king_moves(board_obj, row, col)

    return []


# ================== ATTACK MOVES ==================
def get_attacks(board_obj, row, col):
    piece = board_obj.board[row][col]

    if piece == "":
        return []

    piece_type = piece[1]

    if piece_type == "p":
        return pawn_attacks(board_obj, row, col)
    if piece_type == "k":
        return king_attacks(row, col)

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
                if king_pos in get_attacks(board_obj, r, c):
                    return True

    return False


def build_move(board_obj, start, end):
    r1, c1 = start
    r2, c2 = end

    piece = board_obj.board[r1][c1]
    target = board_obj.board[r2][c2]

    is_en_passant = (
        piece[1] == "p"
        and target == ""
        and c1 != c2
        and board_obj.en_passant_target == (r2, c2)
    )

    is_capture = target != "" or is_en_passant
    promotion = piece[1] == "p" and (r2 == 0 or r2 == 7)
    is_castling = piece[1] == "k" and abs(c2 - c1) == 2

    return Move(
        start,
        end,
        is_capture=is_capture,
        promotion=promotion,
        is_en_passant=is_en_passant,
        is_castling=is_castling,
    )


def castling_path_is_safe(board_obj, color, start, end):
    r1, c1 = start
    r2, c2 = end

    if abs(c2 - c1) != 2:
        return True

    if is_in_check(board_obj, color):
        return False

    step = 1 if c2 > c1 else -1
    mid_col = c1 + step
    mid_move = Move((r1, c1), (r1, mid_col))

    board_obj.make_move(mid_move)
    try:
        return not is_in_check(board_obj, color)
    finally:
        board_obj.undo_move()


# ================== LEGAL MOVES ==================
def get_legal_moves(board_obj, color):
    moves = []

    for r in range(8):
        for c in range(8):
            piece = board_obj.board[r][c]

            if piece == "" or piece[0] != color:
                continue

            for r2, c2 in get_valid_moves(board_obj, r, c):
                target = board_obj.board[r2][c2]

                # never allow capturing the king directly
                if target != "" and target[1] == "k":
                    continue

                move = build_move(board_obj, (r, c), (r2, c2))

                if move.is_castling and not castling_path_is_safe(board_obj, color, move.start, move.end):
                    continue

                board_obj.make_move(move)
                try:
                    if not is_in_check(board_obj, color):
                        moves.append(move)
                finally:
                    board_obj.undo_move()

    return moves


# ================== CHECKMATE ==================
def is_checkmate(board_obj, color):
    return is_in_check(board_obj, color) and len(get_legal_moves(board_obj, color)) == 0


# ================== STALEMATE ==================
def is_stalemate(board_obj, color):
    return not is_in_check(board_obj, color) and len(get_legal_moves(board_obj, color)) == 0
