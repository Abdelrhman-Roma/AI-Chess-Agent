import pygame # دي مكتبة بتستخدمها عشان تعمل واجهة رسومية (GUI) وتعرض اللعبة

from gui.input_handler import handle_mouse_click  # دي فانكشن بتتعامل مع ضغط الماوس (اختيار القطع والحركات)
from gui.assests import load_images               # دي فانكشن بتحميل صور قطع الشطرنج
from game.board import Board                      # ده كلاس البورد (الشطرنج نفسه)

pygame.init() # لازم تشغل pygame قبل ما تستخدمه

#----------- board deminstions ---------------
width,height = 800 , 800  # حجم الشاشة (800x800 بيكسل)
rows,cols = 8 , 8         # عدد الصفوف والأعمدة في الشطرنج
square_size = width//cols # حجم كل مربع = عرض الشاشة / عدد الأعمدة
#-------------------------------------------

#---------- Squares Colors ------------------
white =(240 , 217 , 181) # لون المربعات الفاتحة (RGB)
brown =(181 , 136 , 99)  # لون المربعات الغامقة
#--------------------------------------------

board_obj = Board()      # إنشاء object من البورد
board = board_obj.board  # بنجيب المصفوفة اللي فيها القطع

#----------Make a Window---------------------
screen = pygame.display.set_mode((width,height)) # فتح نافذة اللعبة بالحجم اللي حددناه
pygame.display.set_caption("Chess Game")         # اسم النافذة

clock = pygame.time.Clock()   # علشان نتحكم في سرعة الفريمات (FPS)
images = load_images(square_size) # تحميل صور القطع بالحجم المناسب

def draw_board():
    # دي فانكشن مسؤولة ترسم البورد والقطع
    for row in range(rows):        # loop على الصفوف
        for col in range(cols):   # loop على الأعمدة
            
            color = white if(row + col)%2 == 0 else brown 
            # بيحدد لون المربع (فاتح ولا غامق) حسب المكان
            
            pygame.draw.rect(screen,color,(col *square_size , row *square_size , square_size,square_size))
            # بيرسم المربع في المكان المناسب
            
            # rect parmetar(where draw , use which color ,x-position , y-position , width of square , height of square )
            
            piece = board[row][col] # بنجيب القطعة اللي في المكان ده
            
            if piece != "":  # لو في قطعة (مش فاضي)
                 screen.blit(images[piece],(col*square_size ,row * square_size))
                 # بنرسم صورة القطعة في مكانها

def get_mouse_pos():
    pos = pygame.mouse.get_pos() # بيرجع مكان الماوس (x,y)
    x,y = pos

    row = y // square_size    # نحول ال y لرقم الصف (0 لـ 7)
    col = x // square_size    # نحول ال x لرقم العمود (0 لـ 7)
  
    return row,col  # نرجع المكان في البورد

def highlight_square(row,col):
    # دي فانكشن بترسم إطار أحمر حوالين المربع المختار
    pygame.draw.rect( screen, (255, 0 , 0) , (col * square_size , row * square_size ,square_size ,square_size) ,4)
    # الرقم 4 هنا سمك الإطار

def main(): # دي الفانكشن الأساسية اللي بتشغل اللعبة
    run = True 
    selected_square =None  # مفيش مربع متحدد في الأول
    
    while run: # طول ما اللعبة شغالة
        clock.tick(60)  # يحدد السرعة 60 فريم في الثانية
       
        draw_board() # بيرسم البورد كل فريم (تحديث الشاشة)
        
        if selected_square:  # لو في مربع متحدد
            highlight_square(*selected_square)  # يرسم عليه إطار
        
        pygame.display.update() # يحدث الشاشة ويعرض كل اللي اترسم

        for event in pygame.event.get(): # بيقرأ الأحداث (ماوس / كيبورد / خروج)
            
            if event.type == pygame.QUIT: # لو قفلت اللعبة
                run = False
            
            if event.type ==pygame.MOUSEBUTTONDOWN: # لو ضغطت بالماوس
                row,col = get_mouse_pos()  # نجيب مكان الضغط
                
                selected_square = handle_mouse_click(board_obj,selected_square,row,col)
                # نبعت الداتا لفانكشن التحكم (هي اللي تحدد الحركة)

    pygame.quit() # يقفل pygame لما اللعبة تخلص

main() # تشغيل البرنامج