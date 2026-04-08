import pygame  # بنستورد مكتبة pygame عشان الواجهة والجرافيكس

from ai.minimax import get_ai_move  # بنستورد دالة حركة الـ AI
from ai.heuristics import heuristics_1, heuristics_2, heuristics_3  # بنستورد دوال التقييم
from game.board import Board  # بنستورد كلاس البورد
from game.rules import get_legal_moves, is_checkmate, is_stalemate, is_in_check  # بنستورد قوانين اللعبة
from gui.assests import load_images  # بنستورد تحميل الصور
from gui.input_handler import handle_mouse_click  # بنستورد التعامل مع ضغطات الماوس

pygame.init()  # بنبدأ pygame

# -------- SETTINGS --------  # إعدادات عامة
WIDTH, HEIGHT = 1000, 800  # عرض وارتفاع النافذة
BOARD_WIDTH = 800  # عرض رقعة الشطرنج بس
ROWS, COLS = 8, 8  # عدد الصفوف والأعمدة
SQUARE_SIZE = BOARD_WIDTH // COLS  # حجم كل مربع

WHITE_SQUARE = (238, 238, 210)  # لون المربعات الفاتحة
GREEN_SQUARE = (118, 150, 86)  # لون المربعات الغامقة
SIDE_PANEL_COLOR = (30, 30, 30)  # لون البانل الجانبي
MENU_BG = (20, 20, 20)  # لون خلفية المنيو
HOVER_COLOR = (255, 255, 0)  # لون التظليل
CHECK_COLOR = (255, 0, 0)  # لون الشيك
MOVE_HINT_COLOR = (0, 255, 0)  # لون النقاط بتاعة الحركات

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # بنعمل نافذة اللعبة
pygame.display.set_caption("Chess AI")  # بنحدد اسم النافذة

clock = pygame.time.Clock()  # ساعة للتحكم في الفريمات
images = load_images(SQUARE_SIZE)  # بنحمّل صور القطع

def create_game_state():  # دالة بتعمل الحالة الابتدائية للعبة
    return {  # بترجع ديكشنري فيه كل حالة اللعبة
        "board_obj": Board(),  # البورد نفسها
        "current_turn": "w",  # الدور يبدأ بالأبيض
        "game_over": False,  # اللعبة لسه مخلصتش
        "winner_text": "",  # مفيش نص فايز لسه
        "valid_moves": [],  # الحركات المتاحة الحالية
        "selected_square": None,  # المربع المختار
        "difficulty": None,  # مستوى الصعوبة
        "game_started": False,  # هل اللعبة بدأت
        "white_time": 600.0,  # وقت الأبيض
        "black_time": 600.0,  # وقت الأسود
        "last_time": pygame.time.get_ticks(),  # آخر وقت محدث
    }  # نهاية الحالة

state = create_game_state()  # بننشئ حالة اللعبة

# -------- MENU --------  # دوال المنيو
def draw_menu():  # دالة رسم منيو البداية
    screen.fill(MENU_BG)  # بنلون الخلفية

    title_font = pygame.font.SysFont(None, 60)  # فونت العنوان
    font = pygame.font.SysFont(None, 40)  # فونت الأزرار

    title = title_font.render("Choose Difficulty", True, (255, 255, 255))  # بنرسم عنوان المنيو
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 180)))  # بنعرض العنوان في النص

    mouse_pos = pygame.mouse.get_pos()  # بنجيب مكان الماوس
    buttons = [  # ليستة الأزرار
        ("Easy", (0, 255, 0), 320),  # زر easy
        ("Medium", (255, 255, 0), 400),  # زر medium
        ("Hard", (255, 0, 0), 480),  # زر hard
    ]  # نهاية الأزرار

    rects = []  # ليستة هنحفظ فيها مستطيلات الأزرار

    for text, color, y in buttons:  # بنلف على كل زر
        rect = pygame.Rect(0, 0, 250, 60)  # بنعمل مستطيل للزر
        rect.center = (WIDTH // 2, y)  # بنحطه في النص أفقيًا

        fill_color = (70, 70, 70) if rect.collidepoint(mouse_pos) else (40, 40, 40)  # لون مختلف لو الماوس فوق الزر
        pygame.draw.rect(screen, fill_color, rect, border_radius=10)  # بنرسم الزر

        label = font.render(text, True, color)  # بنرسم النص بتاع الزر
        screen.blit(label, label.get_rect(center=rect.center))  # بنعرض النص جوا الزر

        rects.append((rect, text.lower()))  # بنحفظ المستطيل مع اسم المستوى

    return rects  # بنرجع الأزرار

# -------- DRAW BOARD --------  # رسم البورد
def draw_board(board_obj):  # دالة رسم الرقعة والقطع
    for r in range(ROWS):  # بنلف على الصفوف
        for c in range(COLS):  # بنلف على الأعمدة
            color = WHITE_SQUARE if (r + c) % 2 == 0 else GREEN_SQUARE  # بنحدد لون المربع
            pygame.draw.rect(  # بنرسم المربع
                screen,  # على الشاشة
                color,  # باللون المناسب
                (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),  # مكان وحجم المربع
            )  # نهاية رسم المربع

            piece = board_obj.board[r][c]  # بنجيب القطعة الموجودة
            if piece:  # لو فيه قطعة
                image = images.get(piece)  # بنجيب صورتها
                if image is not None:  # لو الصورة موجودة
                    screen.blit(image, (c * SQUARE_SIZE, r * SQUARE_SIZE))  # بنعرض الصورة

# -------- HIGHLIGHTS --------  # التظليلات
def highlight_moves(moves):  # دالة إظهار الحركات المتاحة
    for r, c in moves:  # بنلف على كل حركة
        pygame.draw.circle(  # بنرسم دايرة
            screen,  # على الشاشة
            MOVE_HINT_COLOR,  # بلون أخضر
            (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2),  # في نص المربع
            10,  # بنصف قطر 10
        )  # نهاية رسم الدايرة

def highlight_check(board_obj, current_turn):  # دالة تظليل الملك لو عليه شيك
    if is_in_check(board_obj, current_turn):  # لو الملك في شيك
        for r in range(8):  # بنلف على الصفوف
            for c in range(8):  # بنلف على الأعمدة
                if board_obj.board[r][c] == current_turn + "k":  # لو ده ملك اللاعب الحالي
                    pygame.draw.rect(  # بنرسم إطار أحمر
                        screen,  # على الشاشة
                        CHECK_COLOR,  # اللون الأحمر
                        (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),  # مكان الملك
                        4,  # سمك الإطار
                    )  # نهاية التظليل

def highlight_hover():  # دالة تظليل المربع اللي الماوس فوقه
    x, y = pygame.mouse.get_pos()  # بنجيب مكان الماوس
    if 0 <= x < BOARD_WIDTH and 0 <= y < HEIGHT:  # لو الماوس جوه البورد
        r = y // SQUARE_SIZE  # بنحسب الصف
        c = x // SQUARE_SIZE  # بنحسب العمود
        pygame.draw.rect(  # بنرسم إطار أصفر
            screen,  # على الشاشة
            HOVER_COLOR,  # اللون الأصفر
            (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),  # مكان المربع
            2,  # سمك الإطار
        )  # نهاية التظليل

def highlight_last_move(board_obj):  # دالة تظليل آخر نقلة
    if board_obj.move_log:  # لو فيه نقلات متسجلة
        move = board_obj.move_log[-1][0]  # بنجيب آخر نقلة

        for r, c in (move.start, move.end):  # بنظلل البداية والنهاية
            pygame.draw.rect(  # بنرسم إطار
                screen,  # على الشاشة
                HOVER_COLOR,  # باللون الأصفر
                (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),  # مكان المربع
                4,  # سمك الإطار
            )  # نهاية التظليل

# -------- TIME --------  # دوال الوقت
def format_time(seconds):  # دالة تنسيق الوقت
    clamped = max(0, int(seconds))  # بنضمن إنه مش سالب
    return f"{clamped // 60:02}:{clamped % 60:02}"  # بنرجعه بصيغة دقائق:ثواني

# -------- SIDE PANEL --------  # رسم البانل الجانبي
def draw_side_panel(difficulty, white_time, black_time):  # دالة رسم المعلومات الجانبية
    pygame.draw.rect(screen, SIDE_PANEL_COLOR, (800, 0, 200, 800))  # بنرسم خلفية البانل

    font = pygame.font.SysFont(None, 32)  # فونت النصوص

    mode = difficulty.upper() if difficulty else "SELECT"  # بنحدد اسم المستوى
    screen.blit(font.render(f"Mode: {mode}", True, (255, 255, 255)), (820, 50))  # بنعرض المستوى
    screen.blit(  # بنعرض وقت الأبيض
        font.render(f"White: {format_time(white_time)}", True, (200, 200, 200)),  # النص
        (820, 150),  # المكان
    )  # نهاية عرض وقت الأبيض
    screen.blit(  # بنعرض وقت الأسود
        font.render(f"Black: {format_time(black_time)}", True, (200, 200, 200)),  # النص
        (820, 200),  # المكان
    )  # نهاية عرض وقت الأسود

# -------- TEXT --------  # عرض رسالة في النص
def draw_text(text):  # دالة عرض رسالة كبيرة
    font = pygame.font.SysFont(None, 70)  # فونت كبير

    bg = pygame.Surface((600, 120))  # خلفية شفافة للنص
    bg.set_alpha(200)  # بنحدد شفافية الخلفية
    bg.fill((0, 0, 0))  # بنلونها أسود

    rect = bg.get_rect(center=(BOARD_WIDTH // 2, HEIGHT // 2))  # بنحط الخلفية في النص
    screen.blit(bg, rect)  # بنعرض الخلفية

    render = font.render(text, True, CHECK_COLOR)  # بنرسم النص
    screen.blit(render, render.get_rect(center=(BOARD_WIDTH // 2, HEIGHT // 2)))  # بنعرض النص

def get_mouse_pos():  # دالة تجيب صف وعمود الماوس
    x, y = pygame.mouse.get_pos()  # بنجيب مكان الماوس
    return y // SQUARE_SIZE, x // SQUARE_SIZE  # بنرجع الصف والعمود

def get_ai_settings(difficulty):  # دالة ترجع إعدادات الـ AI حسب المستوى
    if difficulty == "easy":  # لو easy
        return heuristics_1, 0.2  # بنرجع أول heuristic ووقت قليل
    if difficulty == "medium":  # لو medium
        return heuristics_2, 0.5  # بنرجع الثاني ووقت متوسط
    return heuristics_3, 1.0  # غير كده يبقى hard

def is_terminal_state(board_obj):  # دالة بتشوف هل اللعبة انتهت
    return (  # بنرجع true لو فيه حالة نهاية
        is_checkmate(board_obj, "w")  # لو الأبيض مات
        or is_checkmate(board_obj, "b")  # أو الأسود مات
        or is_stalemate(board_obj, "w")  # أو ستالمت للأبيض
        or is_stalemate(board_obj, "b")  # أو ستالمت للأسود
    )  # نهاية الشرط

def update_game_over_status(board_obj, current_turn):  # دالة تحدد هل اللعبة انتهت والنص المناسب
    if is_checkmate(board_obj, current_turn):  # لو اللاعب الحالي عليه مات
        if current_turn == "w":  # لو الأبيض هو اللي مات
            return True, "BLACK WINS (CHECKMATE)"  # الأسود يكسب
        return True, "WHITE WINS (CHECKMATE)"  # الأبيض يكسب

    if is_stalemate(board_obj, current_turn):  # لو فيه ستالمت
        return True, "DRAW (STALEMATE)"  # تعادل

    return False, ""  # غير كده اللعبة مكملة

# -------- MAIN --------  # الدالة الأساسية
def main():  # بداية اللعبة
    global state  # هنستخدم المتغير العام state

    run = True  # فلاغ تشغيل اللعبة

    while run:  # لوب اللعبة الأساسية
        clock.tick(60)  # 60 فريم في الثانية

        # -------- MENU --------  # جزء المنيو
        if not state["game_started"]:  # لو اللعبة لسه مبدأتش
            rects = draw_menu()  # بنرسم المنيو
            pygame.display.flip()  # بنحدث الشاشة

            for event in pygame.event.get():  # بنقرأ الأحداث
                if event.type == pygame.QUIT:  # لو المستخدم قفل
                    run = False  # نخرج من اللعبة

                elif event.type == pygame.MOUSEBUTTONDOWN:  # لو ضغط ماوس
                    for rect, level in rects:  # بنلف على الأزرار
                        if rect.collidepoint(event.pos):  # لو ضغط على زر
                            state = create_game_state()  # بنعمل حالة جديدة
                            state["difficulty"] = level  # بنحدد المستوى
                            state["game_started"] = True  # نبدأ اللعبة
                            state["last_time"] = pygame.time.get_ticks()  # نصفر توقيت آخر فريم
                            break  # نخرج من لوب الأزرار

            continue  # نرجع لأول اللوب

        # -------- TIMER --------  # تحديث الوقت
        now = pygame.time.get_ticks()  # الوقت الحالي
        delta = (now - state["last_time"]) / 1000.0  # الفرق بالثواني
        state["last_time"] = now  # بنحدث آخر وقت

        if not state["game_over"]:  # لو اللعبة لسه شغالة
            if state["current_turn"] == "w":  # لو دور الأبيض
                state["white_time"] -= delta  # نقلل وقته
            else:  # غير كده دور الأسود
                state["black_time"] -= delta  # نقلل وقته

        # -------- TIME END --------  # لو الوقت خلص
        if state["white_time"] <= 0:  # لو وقت الأبيض خلص
            state["white_time"] = 0  # نثبته على صفر
            state["winner_text"] = "BLACK WINS (TIME)"  # الأسود كسب بالوقت
            state["game_over"] = True  # اللعبة انتهت
        elif state["black_time"] <= 0:  # لو وقت الأسود خلص
            state["black_time"] = 0  # نثبته على صفر
            state["winner_text"] = "WHITE WINS (TIME)"  # الأبيض كسب بالوقت
            state["game_over"] = True  # اللعبة انتهت

        # -------- CHECK GAME END --------  # فحص نهاية اللعبة
        if not state["game_over"]:  # لو اللعبة لسه ما انتهتش
            state["game_over"], state["winner_text"] = update_game_over_status(  # بنحدث حالة النهاية
                state["board_obj"],  # البورد الحالية
                state["current_turn"],  # اللاعب الحالي
            )  # نهاية التحديث

        # -------- DRAW --------  # الرسم على الشاشة
        draw_board(state["board_obj"])  # بنرسم البورد
        highlight_moves(state["valid_moves"])  # بنرسم الحركات المتاحة
        highlight_last_move(state["board_obj"])  # بنظلل آخر نقلة
        highlight_hover()  # بنظلل مكان الماوس
        highlight_check(state["board_obj"], state["current_turn"])  # بنظلل الشيك
        draw_side_panel(  # بنرسم البانل الجانبي
            state["difficulty"],  # المستوى
            state["white_time"],  # وقت الأبيض
            state["black_time"],  # وقت الأسود
        )  # نهاية البانل

        if state["game_over"]:  # لو اللعبة خلصت
            draw_text(state["winner_text"])  # بنعرض النتيجة

        pygame.display.flip()  # بنحدث الشاشة

        # -------- EVENTS --------  # أحداث اللعبة
        for event in pygame.event.get():  # بنقرأ كل الأحداث
            if event.type == pygame.QUIT:  # لو المستخدم قفل اللعبة
                run = False  # نوقف التشغيل

            elif event.type == pygame.MOUSEBUTTONDOWN and not state["game_over"]:  # لو ضغط ماوس واللعبة شغالة
                if state["current_turn"] == "w":  # لو دور الأبيض
                    r, c = get_mouse_pos()  # بنجيب الصف والعمود
                    old_board = [row[:] for row in state["board_obj"].board]  # بننسخ البورد قبل الحركة

                    state["selected_square"] = handle_mouse_click(  # بنعالج الضغطة
                        state["board_obj"],  # البورد
                        state["selected_square"],  # المربع المختار
                        r,  # الصف
                        c,  # العمود
                        state["current_turn"],  # اللاعب الحالي
                    )  # نهاية المعالجة

                    if state["selected_square"]:  # لو فيه مربع متحدد
                        sr, sc = state["selected_square"]  # بناخد مكانه
                        legal_moves = get_legal_moves(state["board_obj"], state["current_turn"])  # بنجيب الحركات القانونية
                        state["valid_moves"] = [  # بنفلتر الحركات الخاصة بالقطعة المختارة
                            move.end for move in legal_moves if move.start == (sr, sc)  # بنجيب النهاية بس
                        ]  # نهاية ليستة الحركات
                    else:  # لو مفيش اختيار
                        state["valid_moves"] = []  # نصفر الحركات

                    if old_board != state["board_obj"].board:  # لو البورد اتغيرت يعني حصلت نقلة
                        state["current_turn"] = "b"  # يبقى الدور على الأسود
                        state["selected_square"] = None  # نشيل الاختيار
                        state["valid_moves"] = []  # نشيل الحركات

                        state["game_over"], state["winner_text"] = update_game_over_status(  # بنفحص هل الأبيض أنهى اللعبة
                            state["board_obj"],  # البورد
                            state["current_turn"],  # اللاعب الجديد
                        )  # نهاية الفحص

        # -------- AI --------  # جزء الـ AI
        if state["current_turn"] == "b" and not state["game_over"]:  # لو دور الأسود واللعبة شغالة
            eval_func, max_time = get_ai_settings(state["difficulty"])  # بنجيب إعدادات الذكاء

            move = get_ai_move(  # بنطلب نقلة من الـ AI
                state["board_obj"],  # البورد
                get_legal_moves,  # دالة الحركات القانونية
                eval_func,  # دالة التقييم
                is_terminal_state,  # دالة فحص نهاية اللعبة
                max_time,  # وقت البحث
            )  # نهاية استدعاء الـ AI

            if move is not None:  # لو الـ AI رجع نقلة
                state["board_obj"].make_move(move)  # ننفذها

            state["current_turn"] = "w"  # يرجع الدور على الأبيض
            state["selected_square"] = None  # نشيل أي اختيار
            state["valid_moves"] = []  # ونفضي الحركات

            state["game_over"], state["winner_text"] = update_game_over_status(  # نفحص هل الأسود أنهى اللعبة
                state["board_obj"],  # البورد
                state["current_turn"],  # اللاعب الحالي
            )  # نهاية الفحص

        if state["game_over"]:  # لو اللعبة انتهت
            state["valid_moves"] = []  # نمسح الحركات
            state["selected_square"] = None  # ونلغي الاختيار

    pygame.quit()  # بنقفل pygame

if __name__ == "__main__":  # لو الملف ده اتشغل مباشر
    main()  # نشغل اللعبة
