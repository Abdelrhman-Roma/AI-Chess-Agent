class Board:
    def __init__(self):
        # إنشاء البورد
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

        self.move_log = []  #  مهم جدا للـ undo

    def get_piece(self, row, col):
        return self.board[row][col]

    #  الفانكشن الأساسية للـ AI
    def make_move(self, move):
        r1, c1 = move.start
        r2, c2 = move.end

        piece = self.board[r1][c1]
        captured = self.board[r2][c2]

        # نحفظ الحركة
        self.move_log.append((move, captured))

        # ننفذ الحركة
        self.board[r2][c2] = piece
        self.board[r1][c1] = ""

    #  أهم حاجة للـ Minimax
    def undo_move(self):
        if not self.move_log:
            return

        move, captured = self.move_log.pop()

        r1, c1 = move.start
        r2, c2 = move.end

        piece = self.board[r2][c2]

        # نرجع الحركة
        self.board[r1][c1] = piece
        self.board[r2][c2] = captured

    # (اختياري) علشان الكود القديم يفضل شغال
    def move_piece(self, move):
        self.make_move(move)