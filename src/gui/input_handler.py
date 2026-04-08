from game.rules import get_legal_moves  # بنستورد دالة الحركات القانونية

def handle_mouse_click(board_obj, selected_square, row, col, turn):  # دالة التعامل مع ضغطة الماوس
    board = board_obj.board  # بنجيب البورد الحالية

    if not (0 <= row < 8 and 0 <= col < 8):  # لو الضغطة بره البورد
        return selected_square  # بنرجع نفس الاختيار زي ما هو

    # Select a piece  # اختيار قطعة
    if selected_square is None:  # لو مفيش قطعة متختارة
        if board[row][col] != "" and board[row][col][0] == turn:  # لو المربع فيه قطعة من نفس لون الدور
            return (row, col)  # بنختارها
        return None  # غير كده مفيش اختيار

    old_row, old_col = selected_square  # بنجيب مكان القطعة المختارة

    # Deselect the same square  # لو ضغطت على نفس المربع نلغي الاختيار
    if (row, col) == selected_square:  # لو نفس المربع
        return None  # نلغي التحديد

    legal_moves = get_legal_moves(board_obj, turn)  # بنجيب كل الحركات القانونية

    for move in legal_moves:  # بنلف على كل الحركات
        if move.start == (old_row, old_col) and move.end == (row, col):  # لو الحركة دي تخص القطعة والمربع المطلوب
            board_obj.make_move(move)  # ننفذ الحركة
            return None  # ونلغي التحديد

    # Switch selection to another friendly piece  # لو ضغطت على قطعة تانية من نفس اللون
    if board[row][col] != "" and board[row][col][0] == turn:  # لو فيه قطعة من نفس اللون
        return (row, col)  # نغير الاختيار ليها

    return selected_square  # لو مفيش حركة ومافيش اختيار جديد نخلي القديم زي ما هو
