import pygame
from ai.minimax import get_ai_move
from ai.heuristics import heuristics_1, heuristics_2, heuristics_3

from gui.input_handler import handle_mouse_click
from gui.assests import load_images
from game.board import Board

from game.rules import (
    get_legal_moves,
    is_checkmate,
    is_stalemate,
    is_in_check
)

pygame.init()

# -------- SETTINGS --------
width, height = 1000, 800
board_width = 800

rows, cols = 8, 8
square_size = board_width // cols

white = (238, 238, 210)
brown = (118, 150, 86)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess AI")

clock = pygame.time.Clock()
images = load_images(square_size)

board_obj = Board()

current_turn = "w"
game_over = False
winner_text = ""

valid_moves = []
selected_square = None

difficulty = None
game_started = False

# -------- TIMER --------
white_time = 600
black_time = 600
last_time = pygame.time.get_ticks()


# -------- MENU --------
def draw_menu():
    screen.fill((20, 20, 20))

    title_font = pygame.font.SysFont(None, 60)
    font = pygame.font.SysFont(None, 40)

    title = title_font.render("Choose Difficulty", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(width // 2, 180)))

    mouse_pos = pygame.mouse.get_pos()

    buttons = [
        ("Easy", (0, 255, 0), 320),
        ("Medium", (255, 255, 0), 400),
        ("Hard", (255, 0, 0), 480)
    ]

    rects = []

    for text, color, y in buttons:
        rect = pygame.Rect(0, 0, 250, 60)
        rect.center = (width // 2, y)

        pygame.draw.rect(screen, (70, 70, 70) if rect.collidepoint(mouse_pos) else (40, 40, 40), rect, border_radius=10)

        label = font.render(text, True, color)
        screen.blit(label, label.get_rect(center=rect.center))

        rects.append((rect, text.lower()))

    return rects


# -------- DRAW BOARD --------
def draw_board():
    for r in range(rows):
        for c in range(cols):
            color = white if (r + c) % 2 == 0 else brown
            pygame.draw.rect(screen, color, (c * square_size, r * square_size, square_size, square_size))

            piece = board_obj.board[r][c]
            if piece:
                screen.blit(images[piece], (c * square_size, r * square_size))


# -------- HIGHLIGHTS --------
def highlight_moves(moves):
    for r, c in moves:
        pygame.draw.circle(screen, (0, 255, 0),
                           (c * square_size + square_size // 2,
                            r * square_size + square_size // 2), 10)


def highlight_check():
    if is_in_check(board_obj, current_turn):
        for r in range(8):
            for c in range(8):
                if board_obj.board[r][c] == current_turn + "k":
                    pygame.draw.rect(screen, (255, 0, 0),
                                     (c * square_size, r * square_size, square_size, square_size), 4)


def highlight_hover():
    x, y = pygame.mouse.get_pos()
    if x < board_width:
        r = y // square_size
        c = x // square_size
        pygame.draw.rect(screen, (255, 255, 0),
                         (c * square_size, r * square_size, square_size, square_size), 2)


def highlight_last_move():
    if board_obj.move_log:
        move = board_obj.move_log[-1][0]
        r, c = move.end
        pygame.draw.rect(screen, (255, 255, 0),
                         (c * square_size, r * square_size, square_size, square_size), 4)


# -------- TIME --------
def format_time(sec):
    return f"{int(sec)//60:02}:{int(sec)%60:02}"


# -------- SIDE PANEL --------
def draw_side_panel():
    pygame.draw.rect(screen, (30, 30, 30), (800, 0, 200, 800))

    font = pygame.font.SysFont(None, 32)

    mode = difficulty.upper() if difficulty else "SELECT"
    screen.blit(font.render(f"Mode: {mode}", True, (255, 255, 255)), (820, 50))
    screen.blit(font.render(f"White: {format_time(white_time)}", True, (200, 200, 200)), (820, 150))
    screen.blit(font.render(f"Black: {format_time(black_time)}", True, (200, 200, 200)), (820, 200))


# -------- TEXT --------
def draw_text(text):
    font = pygame.font.SysFont(None, 70)

    bg = pygame.Surface((600, 120))
    bg.set_alpha(200)
    bg.fill((0, 0, 0))

    rect = bg.get_rect(center=(400, height // 2))
    screen.blit(bg, rect)

    render = font.render(text, True, (255, 0, 0))
    screen.blit(render, render.get_rect(center=(400, height // 2)))


def get_mouse_pos():
    x, y = pygame.mouse.get_pos()
    return y // square_size, x // square_size


# -------- MAIN --------
def main():
    global current_turn, game_over, winner_text
    global valid_moves, selected_square
    global difficulty, game_started
    global white_time, black_time, last_time

    run = True

    while run:
        clock.tick(60)

        # -------- MENU --------
        if not game_started:
            rects = draw_menu()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, level in rects:
                        if rect.collidepoint(pygame.mouse.get_pos()):
                            difficulty = level
                            game_started = True

            continue

        # -------- TIMER --------
        now = pygame.time.get_ticks()
        delta = (now - last_time) / 1000
        last_time = now

        if not game_over:
            if current_turn == "w":
                white_time -= delta
            else:
                black_time -= delta

        # -------- TIME END --------
        if white_time <= 0:
            winner_text = "BLACK WINS (TIME)"
            game_over = True
        elif black_time <= 0:
            winner_text = "WHITE WINS (TIME)"
            game_over = True

        # -------- CHECK GAME END (🔥 FIXED) --------
        if not game_over:
            if is_checkmate(board_obj, current_turn):
                if current_turn == "w":
                    winner_text = "BLACK WINS (CHECKMATE)"
                else:
                    winner_text = "WHITE WINS (CHECKMATE)"

                print(winner_text)
                game_over = True

            elif is_stalemate(board_obj, current_turn):
                winner_text = "DRAW (STALEMATE)"
                print(winner_text)
                game_over = True

        # -------- DRAW --------
        draw_board()
        highlight_moves(valid_moves)
        highlight_last_move()
        highlight_hover()
        highlight_check()
        draw_side_panel()

        if game_over:
            draw_text(winner_text)

        pygame.display.update()

        # -------- EVENTS --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if current_turn == "w":

                    r, c = get_mouse_pos()
                    old_board = [row[:] for row in board_obj.board]

                    selected_square = handle_mouse_click(
                        board_obj, selected_square, r, c, current_turn
                    )

                    if selected_square:
                        sr, sc = selected_square
                        legal_moves = get_legal_moves(board_obj, current_turn)
                        valid_moves = [m.end for m in legal_moves if m.start == (sr, sc)]
                    else:
                        valid_moves = []

                    if old_board != board_obj.board:
                        current_turn = "b"
                        selected_square = None
                        valid_moves = []

        # -------- AI --------
        if current_turn == "b" and not game_over:

            eval_func = heuristics_1 if difficulty == "easy" else heuristics_2 if difficulty == "medium" else heuristics_3
            max_time = 0.2 if difficulty == "easy" else 0.5 if difficulty == "medium" else 1.0

            move = get_ai_move(
                board_obj,
                get_legal_moves,
                eval_func,
                lambda b: is_checkmate(b, "w") or is_checkmate(b, "b"),
                max_time
            )

            if move:
                board_obj.make_move(move)

            current_turn = "w"
            valid_moves = []

    pygame.quit()


main()