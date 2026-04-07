class Board:
    def __init__(self):
        self.board = [
            ["br","bn","bb","bq","bk","bb","bn","br"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["","","","","","","",""],
            ["","","","","","","",""],
            ["","","","","","","",""],
            ["","","","","","","",""],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wr","wn","wb","wq","wk","wb","wn","wr"],
        ]

        self.move_log = []

        self.en_passant_target = None
        self.white_king_moved = False
        self.black_king_moved = False

        self.promotion_choice = "q"

    # ================= MAKE MOVE =================
    def make_move(self, move):
        r1, c1 = move.start
        r2, c2 = move.end

        piece = self.board[r1][c1]
        captured = self.board[r2][c2]

        move.is_capture = captured != ""

        old_en_passant = self.en_passant_target
        old_wkm = self.white_king_moved
        old_bkm = self.black_king_moved

        promotion = False
        en_passant_capture = False
        castling_move = False

        # EN PASSANT
        if piece == "wp" and (r2, c2) == self.en_passant_target:
            captured = self.board[r2+1][c2]
            self.board[r2+1][c2] = ""
            en_passant_capture = True
            move.is_capture = True

        elif piece == "bp" and (r2, c2) == self.en_passant_target:
            captured = self.board[r2-1][c2]
            self.board[r2-1][c2] = ""
            en_passant_capture = True
            move.is_capture = True

        # MOVE
        self.board[r2][c2] = piece
        self.board[r1][c1] = ""

        # PROMOTION
        if piece[1] == "p":
            if piece[0] == "w" and r2 == 0:
                self.board[r2][c2] = "w" + self.promotion_choice
                promotion = True
            elif piece[0] == "b" and r2 == 7:
                self.board[r2][c2] = "b" + self.promotion_choice
                promotion = True

        # EN PASSANT TARGET
        if piece == "wp" and r1 == 6 and r2 == 4:
            self.en_passant_target = (5, c2)
        elif piece == "bp" and r1 == 1 and r2 == 3:
            self.en_passant_target = (2, c2)
        else:
            self.en_passant_target = None

        # CASTLING
        if piece == "wk":
            self.white_king_moved = True
            if abs(c1 - c2) == 2:
                castling_move = True
                if c2 == 6:
                    self.board[7][5] = self.board[7][7]
                    self.board[7][7] = ""
                else:
                    self.board[7][3] = self.board[7][0]
                    self.board[7][0] = ""

        elif piece == "bk":
            self.black_king_moved = True
            if abs(c1 - c2) == 2:
                castling_move = True
                if c2 == 6:
                    self.board[0][5] = self.board[0][7]
                    self.board[0][7] = ""
                else:
                    self.board[0][3] = self.board[0][0]
                    self.board[0][0] = ""

        self.move_log.append((
            move, captured, old_en_passant,
            old_wkm, old_bkm, promotion,
            piece, en_passant_capture, castling_move
        ))

    # ================= UNDO =================
    def undo_move(self):
        if not self.move_log:
            return

        (move, captured, old_en_passant,
         old_wkm, old_bkm, promotion,
         original_piece, en_passant_capture,
         castling_move) = self.move_log.pop()

        r1, c1 = move.start
        r2, c2 = move.end

        if promotion:
            self.board[r1][c1] = original_piece
        else:
            self.board[r1][c1] = self.board[r2][c2]

        self.board[r2][c2] = captured

        if en_passant_capture:
            if original_piece == "wp":
                self.board[r2+1][c2] = "bp"
                self.board[r2][c2] = ""
            else:
                self.board[r2-1][c2] = "wp"
                self.board[r2][c2] = ""

        if castling_move:
            if original_piece == "wk":
                if c2 == 6:
                    self.board[7][7] = self.board[7][5]
                    self.board[7][5] = ""
                else:
                    self.board[7][0] = self.board[7][3]
                    self.board[7][3] = ""
            elif original_piece == "bk":
                if c2 == 6:
                    self.board[0][7] = self.board[0][5]
                    self.board[0][5] = ""
                else:
                    self.board[0][0] = self.board[0][3]
                    self.board[0][3] = ""

        self.en_passant_target = old_en_passant
        self.white_king_moved = old_wkm
        self.black_king_moved = old_bkm

    # ================= CHECK LOGIC =================
    def find_king(self, color):
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == color + "k":
                    return (r, c)
        return None

    def is_in_check(self, color):
        king_pos = self.find_king(color)
        opponent = "b" if color == "w" else "w"

        for r in range(8):
            for c in range(8):
                if self.board[r][c].startswith(opponent):
                    moves = self.get_valid_moves(r, c)
                    if king_pos in moves:
                        return True
        return False

    def has_valid_moves(self, color):
        for r in range(8):
            for c in range(8):
                if self.board[r][c].startswith(color):
                    moves = self.get_valid_moves(r, c)

                    for move in moves:
                        temp = [row[:] for row in self.board]
                        self.make_move(type("Move", (), {"start": (r,c), "end": move}))
                        
                        if not self.is_in_check(color):
                            self.board = temp
                            return True

                        self.board = temp
        return False

    def is_checkmate(self, color):
        return self.is_in_check(color) and not self.has_valid_moves(color)