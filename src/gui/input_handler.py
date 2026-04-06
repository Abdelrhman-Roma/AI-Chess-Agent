from game.rules import get_legal_moves
from game.move import Move


def handle_mouse_click(board_obj, selected_square, row, col, turn):
    # دي الفانكشن اللي بتتعامل مع كل ضغطة ماوس

    board = board_obj.board

    # حماية من الضغط خارج البورد
    if not (0 <= row < 8 and 0 <= col < 8):
        return selected_square

    # ================= SELECT =================
    if selected_square is None:
        # اختار قطعة بس من نفس لون الدور
        if board[row][col] != "" and board[row][col][0] == turn:
            return (row, col)
        return None

    # ================= MOVE =================
    else:
        old_row, old_col = selected_square

        # لو ضغط نفس المربع → فك التحديد
        if (row, col) == selected_square:
            return None

        # نجيب الحركات القانونية فقط
        legal_moves = get_legal_moves(board_obj, turn)

        for move in legal_moves:
            if move.start == (old_row, old_col) and move.end == (row, col):
                board_obj.make_move(move)
                return None

        # لو ضغطت على قطعة تانية من نفس اللون → غيّر الاختيار
        if board[row][col] != "" and board[row][col][0] == turn:
            return (row, col)

        return None