class Board:  # كلاس البورد
    def __init__(self):  # الكونستركتور
        self.board = [  # الشكل الابتدائي للبورد
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],  # الصف الأول للأسود
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],  # صف البيادق السودا
            ["", "", "", "", "", "", "", ""],  # صف فاضي
            ["", "", "", "", "", "", "", ""],  # صف فاضي
            ["", "", "", "", "", "", "", ""],  # صف فاضي
            ["", "", "", "", "", "", "", ""],  # صف فاضي
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],  # صف البيادق البيضا
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],  # الصف الأول للأبيض
        ]  # نهاية البورد

        self.move_log = []  # سجل النقلات
        self.en_passant_target = None  # هدف en passant

        self.white_king_moved = False  # هل الملك الأبيض اتحرك
        self.black_king_moved = False  # هل الملك الأسود اتحرك
        self.white_rook_a_moved = False  # هل القلعة البيضا الشمال اتحركت
        self.white_rook_h_moved = False  # هل القلعة البيضا اليمين اتحركت
        self.black_rook_a_moved = False  # هل القلعة السودا الشمال اتحركت
        self.black_rook_h_moved = False  # هل القلعة السودا اليمين اتحركت

        self.promotion_choice = "q"  # الاختيار الافتراضي للترقية

    # ================= CASTLING RIGHTS =================  # صلاحية الكاستلينج يمين
    def can_castle_kingside(self, color):  # دالة تشوف هل ينفع كاستلينج يمين
        if color == "w":  # لو أبيض
            return (  # نرجع كل الشروط
                not self.white_king_moved  # الملك الأبيض ما اتحركش
                and not self.white_rook_h_moved  # القلعة اليمين ما اتحركتش
                and self.board[7][4] == "wk"  # الملك في مكانه
                and self.board[7][7] == "wr"  # القلعة في مكانها
                and self.board[7][5] == ""  # الخانة بينهما فاضية
                and self.board[7][6] == ""  # الخانة التانية فاضية
            )  # نهاية الشروط

        return (  # لو أسود
            not self.black_king_moved  # الملك الأسود ما اتحركش
            and not self.black_rook_h_moved  # القلعة اليمين ما اتحركتش
            and self.board[0][4] == "bk"  # الملك في مكانه
            and self.board[0][7] == "br"  # القلعة في مكانها
            and self.board[0][5] == ""  # الخانة الأولى فاضية
            and self.board[0][6] == ""  # الخانة التانية فاضية
        )  # نهاية الشروط

    def can_castle_queenside(self, color):  # دالة تشوف هل ينفع كاستلينج شمال
        if color == "w":  # لو أبيض
            return (  # نرجع الشروط
                not self.white_king_moved  # الملك ما اتحركش
                and not self.white_rook_a_moved  # القلعة الشمال ما اتحركتش
                and self.board[7][4] == "wk"  # الملك في مكانه
                and self.board[7][0] == "wr"  # القلعة في مكانها
                and self.board[7][1] == ""  # الخانات بينهم فاضية
                and self.board[7][2] == ""
                and self.board[7][3] == ""
            )  # نهاية الشروط

        return (  # لو أسود
            not self.black_king_moved  # الملك ما اتحركش
            and not self.black_rook_a_moved  # القلعة الشمال ما اتحركتش
            and self.board[0][4] == "bk"  # الملك في مكانه
            and self.board[0][0] == "br"  # القلعة في مكانها
            and self.board[0][1] == ""  # الخانات بينهم فاضية
            and self.board[0][2] == ""
            and self.board[0][3] == ""
        )  # نهاية الشروط

    # ================= MAKE MOVE =================  # تنفيذ النقلة
    def make_move(self, move):  # دالة تنفيذ حركة
        r1, c1 = move.start  # بداية الحركة
        r2, c2 = move.end  # نهاية الحركة

        piece = self.board[r1][c1]  # القطعة اللي هتتحرك
        captured = self.board[r2][c2]  # القطعة المأكولة لو موجودة

        old_state = {  # بنحفظ الحالة القديمة عشان undo
            "en_passant_target": self.en_passant_target,  # هدف en passant القديم
            "white_king_moved": self.white_king_moved,  # حالة الملك الأبيض
            "black_king_moved": self.black_king_moved,  # حالة الملك الأسود
            "white_rook_a_moved": self.white_rook_a_moved,  # القلعة البيضا الشمال
            "white_rook_h_moved": self.white_rook_h_moved,  # القلعة البيضا اليمين
            "black_rook_a_moved": self.black_rook_a_moved,  # القلعة السودا الشمال
            "black_rook_h_moved": self.black_rook_h_moved,  # القلعة السودا اليمين
        }  # نهاية الحالة

        promotion = False  # فلاغ الترقية
        en_passant_capture = False  # فلاغ en passant
        castling_move = piece[1] == "k" and abs(c2 - c1) == 2  # هل الحركة كاستلينج

        move.is_castling = castling_move  # نسجل هل الحركة castling
        move.is_en_passant = False  # نبدأها false
        move.is_capture = captured != ""  # هل فيها أكل

        # en passant capture  # تنفيذ en passant
        if piece == "wp" and self.en_passant_target == (r2, c2) and c1 != c2 and captured == "":  # en passant للأبيض
            captured = self.board[r2 + 1][c2]  # القطعة المأكولة
            self.board[r2 + 1][c2] = ""  # بنشيلها من مكانها
            en_passant_capture = True  # نعلّم إنها حصلت
            move.is_en_passant = True  # نسجل في الحركة
            move.is_capture = True  # ودي أكلة

        elif piece == "bp" and self.en_passant_target == (r2, c2) and c1 != c2 and captured == "":  # en passant للأسود
            captured = self.board[r2 - 1][c2]  # القطعة المأكولة
            self.board[r2 - 1][c2] = ""  # بنشيلها
            en_passant_capture = True  # نعلّم إنها حصلت
            move.is_en_passant = True  # نسجلها
            move.is_capture = True  # أكلة

        # move piece  # نقل القطعة
        self.board[r2][c2] = piece  # بنحط القطعة في المكان الجديد
        self.board[r1][c1] = ""  # ونفضي المكان القديم

        # promotion  # الترقية
        if piece[1] == "p":  # لو بيدق
            if piece[0] == "w" and r2 == 0:  # لو أبيض وصل آخر صف
                self.board[r2][c2] = "w" + self.promotion_choice  # نرقّيه
                promotion = True  # نعلّم إنها ترقية
            elif piece[0] == "b" and r2 == 7:  # لو أسود وصل آخر صف
                self.board[r2][c2] = "b" + self.promotion_choice  # نرقّيه
                promotion = True  # نعلّم إنها ترقية

        move.promotion = promotion  # نسجل الترقية في الحركة

        # en passant target  # تحديد هدف en passant الجديد
        if piece == "wp" and r1 == 6 and r2 == 4:  # لو بيدق أبيض مشي خطوتين
            self.en_passant_target = (5, c1)  # الهدف يبقى في النص
        elif piece == "bp" and r1 == 1 and r2 == 3:  # لو بيدق أسود مشي خطوتين
            self.en_passant_target = (2, c1)  # الهدف يبقى في النص
        else:  # غير كده
            self.en_passant_target = None  # مفيش هدف

        # castling rights from moving pieces  # تحديث حقوق الكاستلينج بسبب الحركة
        if piece == "wk":  # لو الملك الأبيض اتحرك
            self.white_king_moved = True  # خلاص ما ينفعش كاستلينج
        elif piece == "bk":  # لو الملك الأسود اتحرك
            self.black_king_moved = True  # خلاص ما ينفعش كاستلينج
        elif piece == "wr":  # لو قلعة بيضا اتحركت
            if (r1, c1) == (7, 0):  # القلعة الشمال
                self.white_rook_a_moved = True  # نعلّمها
            elif (r1, c1) == (7, 7):  # القلعة اليمين
                self.white_rook_h_moved = True  # نعلّمها
        elif piece == "br":  # لو قلعة سودا اتحركت
            if (r1, c1) == (0, 0):  # القلعة الشمال
                self.black_rook_a_moved = True  # نعلّمها
            elif (r1, c1) == (0, 7):  # القلعة اليمين
                self.black_rook_h_moved = True  # نعلّمها

        # castling rights from captured rooks  # تحديث الحقوق لو قلعة اتاكلت
        if captured == "wr":  # لو القلعة البيضا اتاكلت
            if (r2, c2) == (7, 0):  # وكانت الشمال
                self.white_rook_a_moved = True  # نلغي حقها
            elif (r2, c2) == (7, 7):  # وكانت اليمين
                self.white_rook_h_moved = True  # نلغي حقها
        elif captured == "br":  # لو القلعة السودا اتاكلت
            if (r2, c2) == (0, 0):  # وكانت الشمال
                self.black_rook_a_moved = True  # نلغي حقها
            elif (r2, c2) == (0, 7):  # وكانت اليمين
                self.black_rook_h_moved = True  # نلغي حقها

        # rook move during castling  # تحريك القلعة وقت الكاستلينج
        if castling_move:  # لو الحركة كاستلينج
            if piece == "wk":  # لو الملك أبيض
                if c2 == 6:  # كاستلينج يمين
                    self.board[7][5] = self.board[7][7]  # نحرك القلعة
                    self.board[7][7] = ""  # ونفضي مكانها
                    self.white_rook_h_moved = True  # ونسجل إنها اتحركت
                else:  # كاستلينج شمال
                    self.board[7][3] = self.board[7][0]  # نحرك القلعة
                    self.board[7][0] = ""  # ونفضي مكانها
                    self.white_rook_a_moved = True  # ونسجل الحركة

            elif piece == "bk":  # لو الملك أسود
                if c2 == 6:  # كاستلينج يمين
                    self.board[0][5] = self.board[0][7]  # نحرك القلعة
                    self.board[0][7] = ""  # ونفضي مكانها
                    self.black_rook_h_moved = True  # ونسجلها
                else:  # كاستلينج شمال
                    self.board[0][3] = self.board[0][0]  # نحرك القلعة
                    self.board[0][0] = ""  # ونفضي مكانها
                    self.black_rook_a_moved = True  # ونسجلها

        self.move_log.append(  # بنسجل كل حاجة في اللوج
            (  # بنحفظ tuple
                move,  # الحركة
                captured,  # القطعة المأكولة
                old_state,  # الحالة القديمة
                promotion,  # هل ترقية
                piece,  # القطعة الأصلية
                en_passant_capture,  # هل en passant
                castling_move,  # هل castling
            )  # نهاية التربل
        )  # نهاية الإضافة

    # ================= UNDO =================  # التراجع عن النقلة
    def undo_move(self):  # دالة ترجع آخر حركة
        if not self.move_log:  # لو مفيش سجل
            return  # نخرج

        (  # بنفك آخر عنصر من اللوج
            move,  # الحركة
            captured,  # المأكول
            old_state,  # الحالة القديمة
            promotion,  # فلاغ الترقية
            original_piece,  # القطعة الأصلية
            en_passant_capture,  # فلاغ en passant
            castling_move,  # فلاغ castling
        ) = self.move_log.pop()  # بنشيل آخر حركة

        r1, c1 = move.start  # بداية الحركة
        r2, c2 = move.end  # نهايتها

        if promotion:  # لو كانت ترقية
            self.board[r1][c1] = original_piece  # نرجع البيدق
        else:  # غير كده
            self.board[r1][c1] = self.board[r2][c2]  # نرجع القطعة لمكانها

        self.board[r2][c2] = captured  # نرجع المأكول أو نفرغ المربع

        if en_passant_capture:  # لو كانت en passant
            if original_piece == "wp":  # لو الأبيض هو اللي أكل
                self.board[r2 + 1][c2] = "bp"  # نرجع البيدق الأسود
            else:  # لو الأسود هو اللي أكل
                self.board[r2 - 1][c2] = "wp"  # نرجع البيدق الأبيض
            self.board[r2][c2] = ""  # ونفضي مربع النزول

        if castling_move:  # لو كانت كاستلينج
            if original_piece == "wk":  # لو ملك أبيض
                if c2 == 6:  # كاستلينج يمين
                    self.board[7][7] = self.board[7][5]  # نرجع القلعة
                    self.board[7][5] = ""  # ونفضي مكانها
                else:  # كاستلينج شمال
                    self.board[7][0] = self.board[7][3]  # نرجع القلعة
                    self.board[7][3] = ""  # ونفضي مكانها
            elif original_piece == "bk":  # لو ملك أسود
                if c2 == 6:  # كاستلينج يمين
                    self.board[0][7] = self.board[0][5]  # نرجع القلعة
                    self.board[0][5] = ""  # ونفضي مكانها
                else:  # كاستلينج شمال
                    self.board[0][0] = self.board[0][3]  # نرجع القلعة
                    self.board[0][3] = ""  # ونفضي مكانها

        self.en_passant_target = old_state["en_passant_target"]  # نرجع هدف en passant القديم
        self.white_king_moved = old_state["white_king_moved"]  # نرجع حالة الملك الأبيض
        self.black_king_moved = old_state["black_king_moved"]  # نرجع حالة الملك الأسود
        self.white_rook_a_moved = old_state["white_rook_a_moved"]  # نرجع حالة القلعة البيضا الشمال
        self.white_rook_h_moved = old_state["white_rook_h_moved"]  # نرجع حالة القلعة البيضا اليمين
        self.black_rook_a_moved = old_state["black_rook_a_moved"]  # نرجع حالة القلعة السودا الشمال
        self.black_rook_h_moved = old_state["black_rook_h_moved"]  # نرجع حالة القلعة السودا اليمين

    # ================= HELPERS =================  # دوال مساعدة
    def find_king(self, color):  # دالة مساعدة لإيجاد الملك
        from game.rules import find_king  # استيراد محلي لتجنب circular import
        return find_king(self, color)  # بننادي الدالة الأساسية

    def is_in_check(self, color):  # دالة مساعدة لفحص الشيك
        from game.rules import is_in_check  # استيراد محلي
        return is_in_check(self, color)  # بنرجع النتيجة

    def has_valid_moves(self, color):  # دالة تشوف هل فيه حركات قانونية
        from game.rules import get_legal_moves  # استيراد محلي
        return len(get_legal_moves(self, color)) > 0  # لو فيه حركات يبقى true

    def is_checkmate(self, color):  # دالة مساعدة لفحص المات
        from game.rules import is_checkmate  # استيراد محلي
        return is_checkmate(self, color)  # بنرجع النتيجة

    def is_stalemate(self, color):  # دالة مساعدة لفحص الستالمت
        from game.rules import is_stalemate  # استيراد محلي
        return is_stalemate(self, color)  # بنرجع النتيجة
