class Move:
    def __init__(self ,start ,end):
        # الكونستركتور: بيتنفذ أول ما تعمل object من الكلاس
        
        self.start = start  # دي نقطة البداية (row , col)
        self.end = end      # دي نقطة النهاية (row , col)

    def __repr__(self):
        # دي فانكشن بتحدد شكل الطباعة لما تعمل print للـ object
        
        return f"Move( {self.start} -> {self.end})"
        # هتطبع مثلاً: Move( (6,0) -> (4,0) )