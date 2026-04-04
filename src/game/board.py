class Board:
    def __init__(self):
        # دي الكونستركتور (بتشتغل أول ما تعمل object من الكلاس)
        
        self.board = [
            ["br","bn","bb","bq","bk","bb","bn","br"], # الصف الأول: قطع الأسود (rook, knight, bishop, queen, king...)
            ["bp","bp","bp","bp","bp","bp","bp","bp"], # الصف التاني: بيادق الأسود
            ["","","","","","","",""],                # صف فاضي
            ["","","","","","","",""],                # صف فاضي
            ["","","","","","","",""],                # صف فاضي
            ["","","","","","","",""],                # صف فاضي
            ["wp","wp","wp","wp","wp","wp","wp","wp"], # الصف قبل الأخير: بيادق الأبيض
            ["wr","wn","wb","wq","wk","wb","wn","wr"], # الصف الأخير: قطع الأبيض
        ]
        # كل عنصر في الليستة بيمثل مربع في الشطرنج
        # w = white , b = black
        # r = rook , n = knight , b = bishop , q = queen , k = king , p = pawn

    def get_piece(self ,row ,col):
        # فانكشن بترجع القطعة اللي في مكان معين
        return self.board[row][col]
        # يعني لو قلتله (0,0) هيرجع "br"

    def move_piece(self,move):
        # دي فانكشن بتحرك قطعة من مكان لمكان
        
        r1 , c1 = move.start  # مكان البداية (row , col)
        r2 , c2 = move.end    # مكان النهاية (row , col)

        self.board[r2][c2] = self.board[r1][c1]
        # نحط القطعة في المكان الجديد
        
        self.board[r1][c1] = ""
        # ونفضي المكان القديم (يبقى فاضي)