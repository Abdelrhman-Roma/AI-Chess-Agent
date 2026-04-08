class Move:
    def __init__(self, start, end, is_capture=False, promotion=False,
                 is_en_passant=False, is_castling=False):
        self.start = start
        self.end = end
        self.is_capture = is_capture
        self.promotion = promotion
        self.is_en_passant = is_en_passant
        self.is_castling = is_castling

    def __repr__(self):
        return f"Move({self.start} -> {self.end})"
