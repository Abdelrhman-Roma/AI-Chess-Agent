class Move:  # كلاس بيمثل النقلة
    def __init__(self, start, end, is_capture=False, promotion=False,
                 is_en_passant=False, is_castling=False):  # الكونستركتور بتاع النقلة
        self.start = start  # مربع البداية
        self.end = end  # مربع النهاية
        self.is_capture = is_capture  # هل النقلة فيها أكل
        self.promotion = promotion  # هل فيها ترقية بيدق
        self.is_en_passant = is_en_passant  # هل هي en passant
        self.is_castling = is_castling  # هل هي castling

    def __repr__(self):  # شكل الطباعة بتاع الأوبجكت
        return f"Move({self.start} -> {self.end})"  # بنرجع وصف بسيط للنقلة