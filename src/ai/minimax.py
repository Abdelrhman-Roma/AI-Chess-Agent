import math  # بنستورد math عشان inf
import time  # بنستورد time عشان الوقت

from game.rules import is_checkmate, is_stalemate  # بنستورد فحص المات والستالمت

MATE_SCORE = 100000  # قيمة كبيرة جدًا للمات


# ============================================ 
# Terminal evaluation  # تقييم الحالات النهائية
# ============================================ 
def get_terminal_score(board, depth, evaluate):  # دالة تقييم حالة نهاية اللعبة
    # White checkmated -> Black wins -> very good for AI (Black)  # لو الأبيض مات يبقى ده ممتاز للأسود
    if is_checkmate(board, "w"):  # لو الأبيض متشيكمات
        return -MATE_SCORE + depth  # ندي سكور كبير سالب لأن الأسود أحسن

    # Black checkmated -> White wins -> very bad for AI (Black)  # لو الأسود مات يبقى ده وحش للأسود
    if is_checkmate(board, "b"):  # لو الأسود متشيكمات
        return MATE_SCORE - depth  # ندي سكور كبير موجب لأن الأبيض كسب

    # Draw  # لو تعادل
    if is_stalemate(board, "w") or is_stalemate(board, "b"):  # لو فيه ستالمت لأي طرف
        return 0  # السكور صفر

    return evaluate(board)  # غير كده نستخدم دالة التقييم العادية


# ============================================  
# Minimax + Alpha-Beta  # مينيماكس مع تقليم ألفا بيتا
# ============================================  
def minimax_alpha_beta(  # دالة البحث الأساسية
    board,  # البورد الحالية
    depth,  # العمق
    alpha,  # ألفا
    beta,  # بيتا
    is_ai_turn,  # هل ده دور الـ AI
    get_legal_moves,  # دالة الحركات القانونية
    evaluate,  # دالة التقييم
    is_game_over,  # دالة فحص نهاية اللعبة
    start_time,  # وقت بداية البحث
    time_limit,  # أقصى وقت للبحث
):  # نهاية التعريف
    if time.time() - start_time > time_limit:  # لو الوقت خلص
        return evaluate(board), None, True  # نرجع تقييم سريع ونقول إن فيه timeout

    if depth == 0 or is_game_over(board):  # لو وصلنا لآخر عمق أو اللعبة انتهت
        return get_terminal_score(board, depth, evaluate), None, False  # نرجع تقييم النهاية

    current_color = "b" if is_ai_turn else "w"  # بنحدد لون اللاعب الحالي
    moves = get_legal_moves(board, current_color)  # بنجيب كل الحركات القانونية

    if not moves:  # لو مفيش حركات
        return get_terminal_score(board, depth, evaluate), None, False  # نرجع تقييم نهائي

    def score_move(move):  # دالة لترتيب الحركات
        score = 0  # بنبدأ من صفر

        if getattr(move, "promotion", False):  # لو فيها ترقية
            score += 200  # نديها أولوية أعلى

        if getattr(move, "is_capture", False):  # لو فيها أكل
            score += 100  # نديها أولوية

        if getattr(move, "is_castling", False):  # لو فيها كاستلينج
            score += 50  # نديها شوية أولوية

        return score  # نرجع سكور الحركة

    moves = sorted(moves, key=score_move, reverse=True)  # بنرتب الحركات من الأفضل للأسوأ
    best_move = None  # أحسن حركة لسه غير معروفة

    # AI is Black, and evaluation is White-positive / Black-negative  # الـ AI بيلعب أسود والتقييم موجب للأبيض
    # so Black should minimize the score.  # فبالتالي الأسود لازم يقلل السكور
    if is_ai_turn:  # لو ده دور الـ AI
        best_eval = math.inf  # نبدأ بأكبر قيمة ممكنة

        for move in moves:  # بنلف على كل حركة
            board.make_move(move)  # بننفذ الحركة
            try:  # بنبدأ try
                eval_score, _, timed_out = minimax_alpha_beta(  # بنعمل نداء recursive
                    board,  # نفس البورد بعد الحركة
                    depth - 1,  # عمق أقل
                    alpha,  # ألفا الحالية
                    beta,  # بيتا الحالية
                    False,  # الدور الجاي للمنافس
                    get_legal_moves,  # دالة الحركات
                    evaluate,  # دالة التقييم
                    is_game_over,  # دالة فحص النهاية
                    start_time,  # وقت البداية
                    time_limit,  # الوقت المسموح
                )  # نهاية النداء
            finally:  # مهما حصل
                board.undo_move()  # بنرجع الحركة

            if timed_out:  # لو حصل timeout
                return best_eval, best_move, True  # نرجع أفضل نتيجة وصلنالها

            if getattr(move, "is_capture", False):  # لو الحركة كانت أكلة
                eval_score -= 30  # ندي بونس بسيط للأسود لأنه بيقلل السكور

            if eval_score < best_eval:  # لو النتيجة دي أحسن للأسود
                best_eval = eval_score  # نحدّث أفضل تقييم
                best_move = move  # ونحفظ الحركة

            beta = min(beta, best_eval)  # نحدّث بيتا

            if beta <= alpha:  # لو حصل cut-off
                break  # نوقف بقية الحركات

        return best_eval, best_move, False  # نرجع أفضل نتيجة للأسود

    # White should maximize the score.  # الأبيض لازم يكبر السكور
    best_eval = -math.inf  # نبدأ بأقل قيمة ممكنة

    for move in moves:  # بنلف على كل حركة
        board.make_move(move)  # بننفذ الحركة
        try:  # بنبدأ try
            eval_score, _, timed_out = minimax_alpha_beta(  # نداء recursive
                board,  # نفس البورد
                depth - 1,  # عمق أقل
                alpha,  # ألفا
                beta,  # بيتا
                True,  # الدور الجاي للـ AI
                get_legal_moves,  # دالة الحركات
                evaluate,  # دالة التقييم
                is_game_over,  # دالة فحص النهاية
                start_time,  # وقت البداية
                time_limit,  # الوقت المتاح
            )  # نهاية النداء
        finally:  # مهما حصل
            board.undo_move()  # بنرجع الحركة

        if timed_out:  # لو الوقت خلص
            return best_eval, best_move, True  # نرجع أفضل حاجة لحد هنا

        if getattr(move, "is_capture", False):  # لو الحركة أكلة
            eval_score += 30  # ندي بونس بسيط للأبيض

        if eval_score > best_eval:  # لو النتيجة دي أحسن للأبيض
            best_eval = eval_score  # نحدّث أفضل تقييم
            best_move = move  # نحفظ أحسن حركة

        alpha = max(alpha, best_eval)  # نحدّث ألفا

        if beta <= alpha:  # لو حصل cut-off
            break  # نوقف بقية الحركات

    return best_eval, best_move, False  # نرجع أفضل نتيجة للأبيض


# ============================================ 
# Iterative deepening  # البحث التدريجي بالعمق
# ============================================  
def get_ai_move(board, get_legal_moves, evaluate, is_game_over, max_time=1.0):  # دالة ترجع أحسن حركة للـ AI
    start_time = time.time()  # بنسجل بداية الوقت
    best_move = None  # أحسن حركة لسه غير معروفة
    depth = 1  # بنبدأ من عمق 1

    while True:  # لوب لزيادة العمق تدريجيًا
        if time.time() - start_time > max_time:  # لو الوقت خلص
            break  # نوقف البحث

        _, move, timed_out = minimax_alpha_beta(  # بنشغل المينيماكس
            board,  # البورد الحالية
            depth,  # العمق الحالي
            -math.inf,  # ألفا الابتدائية
            math.inf,  # بيتا الابتدائية
            True,  # دور الـ AI
            get_legal_moves,  # دالة الحركات
            evaluate,  # دالة التقييم
            is_game_over,  # دالة فحص النهاية
            start_time,  # وقت البداية
            max_time,  # الوقت الأقصى
        )  # نهاية الاستدعاء

        if timed_out:  # لو البحث الأخير وقف بسبب الوقت
            break  # نكتفي بآخر نتيجة سليمة

        if move is not None:  # لو لقينا حركة صالحة
            best_move = move  # نخزنها كأفضل حركة

        depth += 1  # نزود العمق واحدة

    return best_move  # نرجع أفضل حركة وصلنالها
