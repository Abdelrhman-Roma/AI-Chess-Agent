from game.piece import (  # بنستورد دوال الحركات من ملف القطع
    pawn_moves,  # حركات البيدق
    rook_moves,  # حركات القلعة
    knight_moves,  # حركات الحصان
    bishop_moves,  # حركات الفيل
    queen_moves,  # حركات الوزير
    king_moves,  # حركات الملك
    pawn_attacks,  # مربعات هجوم البيدق
    king_attacks,  # مربعات هجوم الملك
)  # نهاية الاستيراد
from game.move import Move  # بنستورد كلاس Move


# ================== VALID MOVES ==================  # الحركات المبدئية للقطعة
def get_valid_moves(board_obj, row, col):  # دالة تجيب حركات القطعة حسب نوعها
    board = board_obj.board  # بنجيب البورد
    piece = board[row][col]  # بنجيب القطعة

    if piece == "":  # لو مفيش قطعة
        return []  # نرجع ليستة فاضية

    piece_type = piece[1]  # نوع القطعة

    if piece_type == "p":  # لو بيدق
        return pawn_moves(board_obj, row, col)  # نرجع حركاته
    if piece_type == "r":  # لو قلعة
        return rook_moves(board, row, col)  # نرجع حركاتها
    if piece_type == "n":  # لو حصان
        return knight_moves(board, row, col)  # نرجع حركاته
    if piece_type == "b":  # لو فيل
        return bishop_moves(board, row, col)  # نرجع حركاته
    if piece_type == "q":  # لو وزير
        return queen_moves(board, row, col)  # نرجع حركاته
    if piece_type == "k":  # لو ملك
        return king_moves(board_obj, row, col)  # نرجع حركاته

    return []  # لو نوع غير معروف نرجع فاضي


# ================== ATTACK MOVES ==================  # مربعات التهديد
def get_attacks(board_obj, row, col):  # دالة تجيب مربعات الهجوم للقطعة
    piece = board_obj.board[row][col]  # بنجيب القطعة

    if piece == "":  # لو المربع فاضي
        return []  # نرجع فاضي

    piece_type = piece[1]  # نوع القطعة

    if piece_type == "p":  # لو بيدق
        return pawn_attacks(board_obj, row, col)  # نرجع تهديداته
    if piece_type == "k":  # لو ملك
        return king_attacks(row, col)  # نرجع المربعات اللي حواليه

    return get_valid_moves(board_obj, row, col)  # باقي القطع هجومها = حركتها


# ================== FIND KING ==================  # البحث عن الملك
def find_king(board_obj, color):  # دالة تدور على الملك حسب اللون
    for r in range(8):  # بنلف على الصفوف
        for c in range(8):  # بنلف على الأعمدة
            if board_obj.board[r][c] == color + "k":  # لو لقينا الملك
                return (r, c)  # نرجع مكانه
    return None  # لو مش موجود


# ================== CHECK ==================  # فحص الشيك
def is_in_check(board_obj, color):  # دالة تشوف هل الملك في شيك
    king_pos = find_king(board_obj, color)  # بنجيب مكان الملك

    if king_pos is None:  # لو الملك مش موجود
        return True  # نعتبره في خطر

    enemy = "b" if color == "w" else "w"  # بنحدد لون الخصم

    for r in range(8):  # بنلف على البورد
        for c in range(8):  # بنلف على الأعمدة
            piece = board_obj.board[r][c]  # بنجيب القطعة
            if piece != "" and piece[0] == enemy:  # لو قطعة للخصم
                if king_pos in get_attacks(board_obj, r, c):  # لو الملك ضمن تهديداتها
                    return True  # يبقى في شيك

    return False  # غير كده مفيش شيك


def build_move(board_obj, start, end):  # دالة تبني Move object جاهز
    r1, c1 = start  # البداية
    r2, c2 = end  # النهاية

    piece = board_obj.board[r1][c1]  # القطعة اللي هتتحرك
    target = board_obj.board[r2][c2]  # القطعة الموجودة في الهدف

    is_en_passant = (  # بنحدد هل دي en passant
        piece[1] == "p"  # لازم تكون بيدق
        and target == ""  # والهدف فاضي
        and c1 != c2  # والحركة قطرية
        and board_obj.en_passant_target == (r2, c2)  # ومكان الهدف هو هدف en passant
    )  # نهاية الشرط

    is_capture = target != "" or is_en_passant  # الأكلة لو فيه قطعة أو en passant
    promotion = piece[1] == "p" and (r2 == 0 or r2 == 7)  # ترقية لو بيدق وصل آخر صف
    is_castling = piece[1] == "k" and abs(c2 - c1) == 2  # كاستلينج لو الملك اتحرك خانتين

    return Move(  # بنرجع أوبجكت Move
        start,  # البداية
        end,  # النهاية
        is_capture=is_capture,  # هل فيها أكل
        promotion=promotion,  # هل فيها ترقية
        is_en_passant=is_en_passant,  # هل en passant
        is_castling=is_castling,  # هل castling
    )  # نهاية إنشاء النقلة


def castling_path_is_safe(board_obj, color, start, end):  # دالة تتأكد إن طريق الكاستلينج آمن
    r1, c1 = start  # البداية
    r2, c2 = end  # النهاية

    if abs(c2 - c1) != 2:  # لو الحركة مش كاستلينج
        return True  # يبقى مفيش مشكلة

    if is_in_check(board_obj, color):  # لو الملك عليه شيك أصلًا
        return False  # الكاستلينج ممنوع

    step = 1 if c2 > c1 else -1  # بنحدد اتجاه حركة الملك
    mid_col = c1 + step  # العمود الوسيط
    mid_move = Move((r1, c1), (r1, mid_col))  # بنعمل حركة مؤقتة للمربع النص

    board_obj.make_move(mid_move)  # بننفذ الحركة المؤقتة
    try:  # بنبدأ try
        return not is_in_check(board_obj, color)  # لو المربع النص آمن يبقى تمام
    finally:  # مهما حصل
        board_obj.undo_move()  # بنرجع الحركة


# ================== LEGAL MOVES ==================  # الحركات القانونية النهائية
def get_legal_moves(board_obj, color):  # دالة تجيب كل الحركات القانونية للاعب
    moves = []  # ليستة الحركات

    for r in range(8):  # بنلف على الصفوف
        for c in range(8):  # بنلف على الأعمدة
            piece = board_obj.board[r][c]  # بنجيب القطعة

            if piece == "" or piece[0] != color:  # لو المربع فاضي أو مش من نفس اللون
                continue  # نكمل على اللي بعده

            for r2, c2 in get_valid_moves(board_obj, r, c):  # بنلف على الحركات المبدئية
                target = board_obj.board[r2][c2]  # بنجيب الهدف

                # never allow capturing the king directly  # ممنوع تاكل الملك مباشرة
                if target != "" and target[1] == "k":  # لو الهدف ملك
                    continue  # نسيب الحركة دي

                move = build_move(board_obj, (r, c), (r2, c2))  # بنبني الحركة

                if move.is_castling and not castling_path_is_safe(board_obj, color, move.start, move.end):  # لو كاستلينج والطريق مش آمن
                    continue  # نرفض الحركة

                board_obj.make_move(move)  # بننفذ الحركة مؤقتًا
                try:  # بنبدأ try
                    if not is_in_check(board_obj, color):  # لو بعد الحركة الملك مش في شيك
                        moves.append(move)  # نضيف الحركة
                finally:  # مهما حصل
                    board_obj.undo_move()  # نرجع الحركة

    return moves  # نرجع كل الحركات القانونية


# ================== CHECKMATE ==================  # فحص المات
def is_checkmate(board_obj, color):  # دالة تشوف هل اللاعب مات
    return is_in_check(board_obj, color) and len(get_legal_moves(board_obj, color)) == 0  # شيك + مفيش حركات


# ================== STALEMATE ==================  # فحص الستالمت
def is_stalemate(board_obj, color):  # دالة تشوف هل فيه ستالمت
    return not is_in_check(board_obj, color) and len(get_legal_moves(board_obj, color)) == 0  # مفيش شيك + مفيش حركات
