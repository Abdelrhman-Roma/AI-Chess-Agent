def in_bounds(r, c):  # دالة بتتأكد إن المكان جوه البورد
    return 0 <= r < 8 and 0 <= c < 8  # بترجع true لو الصف والعمود صالحين


# ================= PAWN =================  # حركات البيدق
def pawn_moves(board_obj, r, c):  # دالة حركات البيدق
    board = board_obj.board  # بنجيب البورد
    piece = board[r][c]  # بنجيب القطعة
    moves = []  # ليستة الحركات

    direction = -1 if piece[0] == "w" else 1  # اتجاه البيدق حسب اللون
    enemy = "b" if piece[0] == "w" else "w"  # لون الخصم
    one_step_row = r + direction  # الصف بعد خطوة واحدة

    # move forward  # حركة لقدام
    if in_bounds(one_step_row, c) and board[one_step_row][c] == "":  # لو الخانة قدام جوه البورد وفاضية
        moves.append((one_step_row, c))  # نضيف الحركة

        start_row = 6 if piece[0] == "w" else 1  # الصف الابتدائي للبيدق
        two_step_row = r + 2 * direction  # الصف بعد خطوتين
        if r == start_row and in_bounds(two_step_row, c) and board[two_step_row][c] == "":  # لو أول حركة والخانتين صالحين
            moves.append((two_step_row, c))  # نضيف حركة الخطوتين

    # captures  # الأكل
    for dc in (-1, 1):  # يمين وشمال قطري
        nr, nc = r + direction, c + dc  # الصف والعمود الجديدين
        if in_bounds(nr, nc) and board[nr][nc] != "" and board[nr][nc][0] == enemy:  # لو فيه قطعة خصم
            moves.append((nr, nc))  # نضيف الأكلة

    # en passant  # الأخذ بالتجاوز
    if board_obj.en_passant_target:  # لو فيه هدف en passant
        target_r, target_c = board_obj.en_passant_target  # بناخد الهدف
        if target_r == r + direction and abs(target_c - c) == 1:  # لو الهدف مناسب للبيدق ده
            adjacent_piece = board[r][target_c]  # بنجيب القطعة اللي جنب البيدق
            if adjacent_piece == enemy + "p":  # لو فعلاً بيدق خصم
                moves.append((target_r, target_c))  # نضيف الحركة

    return moves  # نرجع كل الحركات


# ================= PAWN ATTACKS =================  # مربعات هجوم البيدق
def pawn_attacks(board_obj, r, c):  # دالة مربعات هجوم البيدق
    board = board_obj.board  # بنجيب البورد
    piece = board[r][c]  # بنجيب القطعة
    moves = []  # ليستة الهجوم

    direction = -1 if piece[0] == "w" else 1  # اتجاه البيدق

    for dc in (-1, 1):  # الاتجاهين القطريين
        nr, nc = r + direction, c + dc  # المكان الجديد
        if in_bounds(nr, nc):  # لو جوه البورد
            moves.append((nr, nc))  # نضيف مربع الهجوم

    return moves  # نرجع مربعات الهجوم


# ================= ROOK =================  # حركات القلعة
def rook_moves(board, r, c):  # دالة حركات القلعة
    moves = []  # ليستة الحركات
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # الاتجاهات الأربعة

    for dr, dc in directions:  # بنلف على الاتجاهات
        for i in range(1, 8):  # بنمشي لحد 7 خانات
            nr, nc = r + dr * i, c + dc * i  # المكان الجديد
            if not in_bounds(nr, nc):  # لو بره البورد
                break  # نوقف الاتجاه ده

            if board[nr][nc] == "":  # لو الخانة فاضية
                moves.append((nr, nc))  # نضيفها
            else:  # لو فيه قطعة
                if board[nr][nc][0] != board[r][c][0]:  # لو قطعة خصم
                    moves.append((nr, nc))  # نضيف الأكلة
                break  # وبعدها نوقف الاتجاه

    return moves  # نرجع الحركات


# ================= KNIGHT =================  # حركات الحصان
def knight_moves(board, r, c):  # دالة حركات الحصان
    moves = []  # ليستة الحركات
    steps = [  # كل قفزات الحصان
        (2, 1), (2, -1), (-2, 1), (-2, -1),  # تحت/فوق مع يمين/شمال
        (1, 2), (1, -2), (-1, 2), (-1, -2),  # يمين/شمال مع فوق/تحت
    ]  # نهاية الخطوات

    for dr, dc in steps:  # بنلف على كل خطوة
        nr, nc = r + dr, c + dc  # المكان الجديد
        if in_bounds(nr, nc):  # لو جوه البورد
            if board[nr][nc] == "" or board[nr][nc][0] != board[r][c][0]:  # لو فاضي أو خصم
                moves.append((nr, nc))  # نضيف الحركة

    return moves  # نرجع الحركات


# ================= BISHOP =================  # حركات الفيل
def bishop_moves(board, r, c):  # دالة حركات الفيل
    moves = []  # ليستة الحركات
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # الاتجاهات القطرية

    for dr, dc in directions:  # بنلف على الاتجاهات
        for i in range(1, 8):  # بنمشي لحد 7 خانات
            nr, nc = r + dr * i, c + dc * i  # المكان الجديد
            if not in_bounds(nr, nc):  # لو بره البورد
                break  # نوقف الاتجاه ده

            if board[nr][nc] == "":  # لو الخانة فاضية
                moves.append((nr, nc))  # نضيفها
            else:  # لو فيه قطعة
                if board[nr][nc][0] != board[r][c][0]:  # لو خصم
                    moves.append((nr, nc))  # نضيف الأكلة
                break  # وبعدها نوقف الاتجاه

    return moves  # نرجع الحركات


# ================= QUEEN =================  # حركات الوزير
def queen_moves(board, r, c):  # دالة حركات الوزير
    return rook_moves(board, r, c) + bishop_moves(board, r, c)  # الوزير = قلعة + فيل


# ================= KING ATTACKS =================  # مربعات هجوم الملك
def king_attacks(r, c):  # دالة مربعات الملك حواليه
    moves = []  # ليستة الهجوم

    for dr in (-1, 0, 1):  # كل فروق الصف
        for dc in (-1, 0, 1):  # كل فروق العمود
            if dr == 0 and dc == 0:  # نفس المربع
                continue  # نتخطاه

            nr, nc = r + dr, c + dc  # المكان الجديد
            if in_bounds(nr, nc):  # لو جوه البورد
                moves.append((nr, nc))  # نضيفه

    return moves  # نرجع المربعات


# ================= KING =================  # حركات الملك
def king_moves(board_obj, r, c):  # دالة حركات الملك
    board = board_obj.board  # بنجيب البورد
    piece = board[r][c]  # بنجيب الملك
    moves = []  # ليستة الحركات

    for nr, nc in king_attacks(r, c):  # بنلف على المربعات حواليه
        if board[nr][nc] == "" or board[nr][nc][0] != piece[0]:  # لو فاضي أو خصم
            moves.append((nr, nc))  # نضيف الحركة

    color = piece[0]  # لون الملك

    # castling availability is checked more deeply in rules.py  # الكاستلينج بيتراجع عليه تاني في rules
    if color == "w":  # لو الملك أبيض
        if board_obj.can_castle_kingside("w"):  # لو ينفع كاستلينج ناحية اليمين
            moves.append((7, 6))  # نضيفها
        if board_obj.can_castle_queenside("w"):  # لو ينفع ناحية الشمال
            moves.append((7, 2))  # نضيفها
    else:  # لو الملك أسود
        if board_obj.can_castle_kingside("b"):  # لو ينفع كاستلينج يمين
            moves.append((0, 6))  # نضيفها
        if board_obj.can_castle_queenside("b"):  # لو ينفع شمال
            moves.append((0, 2))  # نضيفها

    return moves  # نرجع كل الحركات
