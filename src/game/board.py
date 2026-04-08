class Board:
    def __init__(self):
        self.board = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
        ]

        self.move_log = []
        self.en_passant_target = None

        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rook_a_moved = False
        self.white_rook_h_moved = False
        self.black_rook_a_moved = False
        self.black_rook_h_moved = False

        self.promotion_choice = "q"

    # ================= CASTLING RIGHTS =================
    def can_castle_kingside(self, color):
        if color == "w":
            return (
                not self.white_king_moved
                and not self.white_rook_h_moved
                and self.board[7][4] == "wk"
                and self.board[7][7] == "wr"
                and self.board[7][5] == ""
                and self.board[7][6] == ""
            )

        return (
            not self.black_king_moved
            and not self.black_rook_h_moved
            and self.board[0][4] == "bk"
            and self.board[0][7] == "br"
            and self.board[0][5] == ""
            and self.board[0][6] == ""
        )

    def can_castle_queenside(self, color):
        if color == "w":
            return (
                not self.white_king_moved
                and not self.white_rook_a_moved
                and self.board[7][4] == "wk"
                and self.board[7][0] == "wr"
                and self.board[7][1] == ""
                and self.board[7][2] == ""
                and self.board[7][3] == ""
            )

        return (
            not self.black_king_moved
            and not self.black_rook_a_moved
            and self.board[0][4] == "bk"
            and self.board[0][0] == "br"
            and self.board[0][1] == ""
            and self.board[0][2] == ""
            and self.board[0][3] == ""
        )

    # ================= MAKE MOVE =================
    def make_move(self, move):
        r1, c1 = move.start
        r2, c2 = move.end

        piece = self.board[r1][c1]
        captured = self.board[r2][c2]

        old_state = {
            "en_passant_target": self.en_passant_target,
            "white_king_moved": self.white_king_moved,
            "black_king_moved": self.black_king_moved,
            "white_rook_a_moved": self.white_rook_a_moved,
            "white_rook_h_moved": self.white_rook_h_moved,
            "black_rook_a_moved": self.black_rook_a_moved,
            "black_rook_h_moved": self.black_rook_h_moved,
        }

        promotion = False
        en_passant_capture = False
        castling_move = piece[1] == "k" and abs(c2 - c1) == 2

        move.is_castling = castling_move
        move.is_en_passant = False
        move.is_capture = captured != ""

        # en passant capture
        if piece == "wp" and self.en_passant_target == (r2, c2) and c1 != c2 and captured == "":
            captured = self.board[r2 + 1][c2]
            self.board[r2 + 1][c2] = ""
            en_passant_capture = True
            move.is_en_passant = True
            move.is_capture = True

        elif piece == "bp" and self.en_passant_target == (r2, c2) and c1 != c2 and captured == "":
            captured = self.board[r2 - 1][c2]
            self.board[r2 - 1][c2] = ""
            en_passant_capture = True
            move.is_en_passant = True
            move.is_capture = True

        # move piece
        self.board[r2][c2] = piece
        self.board[r1][c1] = ""

        # promotion
        if piece[1] == "p":
            if piece[0] == "w" and r2 == 0:
                self.board[r2][c2] = "w" + self.promotion_choice
                promotion = True
            elif piece[0] == "b" and r2 == 7:
                self.board[r2][c2] = "b" + self.promotion_choice
                promotion = True

        move.promotion = promotion

        # en passant target
        if piece == "wp" and r1 == 6 and r2 == 4:
            self.en_passant_target = (5, c1)
        elif piece == "bp" and r1 == 1 and r2 == 3:
            self.en_passant_target = (2, c1)
        else:
            self.en_passant_target = None

        # castling rights from moving pieces
        if piece == "wk":
            self.white_king_moved = True
        elif piece == "bk":
            self.black_king_moved = True
        elif piece == "wr":
            if (r1, c1) == (7, 0):
                self.white_rook_a_moved = True
            elif (r1, c1) == (7, 7):
                self.white_rook_h_moved = True
        elif piece == "br":
            if (r1, c1) == (0, 0):
                self.black_rook_a_moved = True
            elif (r1, c1) == (0, 7):
                self.black_rook_h_moved = True

        # castling rights from captured rooks
        if captured == "wr":
            if (r2, c2) == (7, 0):
                self.white_rook_a_moved = True
            elif (r2, c2) == (7, 7):
                self.white_rook_h_moved = True
        elif captured == "br":
            if (r2, c2) == (0, 0):
                self.black_rook_a_moved = True
            elif (r2, c2) == (0, 7):
                self.black_rook_h_moved = True

        # rook move during castling
        if castling_move:
            if piece == "wk":
                if c2 == 6:
                    self.board[7][5] = self.board[7][7]
                    self.board[7][7] = ""
                    self.white_rook_h_moved = True
                else:
                    self.board[7][3] = self.board[7][0]
                    self.board[7][0] = ""
                    self.white_rook_a_moved = True

            elif piece == "bk":
                if c2 == 6:
                    self.board[0][5] = self.board[0][7]
                    self.board[0][7] = ""
                    self.black_rook_h_moved = True
                else:
                    self.board[0][3] = self.board[0][0]
                    self.board[0][0] = ""
                    self.black_rook_a_moved = True

        self.move_log.append(
            (
                move,
                captured,
                old_state,
                promotion,
                piece,
                en_passant_capture,
                castling_move,
            )
        )

    # ================= UNDO =================
    def undo_move(self):
        if not self.move_log:
            return

        (
            move,
            captured,
            old_state,
            promotion,
            original_piece,
            en_passant_capture,
            castling_move,
        ) = self.move_log.pop()

        r1, c1 = move.start
        r2, c2 = move.end

        if promotion:
            self.board[r1][c1] = original_piece
        else:
            self.board[r1][c1] = self.board[r2][c2]

        self.board[r2][c2] = captured

        if en_passant_capture:
            if original_piece == "wp":
                self.board[r2 + 1][c2] = "bp"
            else:
                self.board[r2 - 1][c2] = "wp"
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

        self.en_passant_target = old_state["en_passant_target"]
        self.white_king_moved = old_state["white_king_moved"]
        self.black_king_moved = old_state["black_king_moved"]
        self.white_rook_a_moved = old_state["white_rook_a_moved"]
        self.white_rook_h_moved = old_state["white_rook_h_moved"]
        self.black_rook_a_moved = old_state["black_rook_a_moved"]
        self.black_rook_h_moved = old_state["black_rook_h_moved"]

    # ================= HELPERS =================
    def find_king(self, color):
        from game.rules import find_king
        return find_king(self, color)

    def is_in_check(self, color):
        from game.rules import is_in_check
        return is_in_check(self, color)

    def has_valid_moves(self, color):
        from game.rules import get_legal_moves
        return len(get_legal_moves(self, color)) > 0

    def is_checkmate(self, color):
        from game.rules import is_checkmate
        return is_checkmate(self, color)

    def is_stalemate(self, color):
        from game.rules import is_stalemate
        return is_stalemate(self, color)
