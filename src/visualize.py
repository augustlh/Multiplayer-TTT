import pygame
import threading

BG_COLOR = (35, 35, 35)
HL_COLOR = (60, 60, 60)

game_state = None
should_stop = False

move_condition = threading.Condition()
needs_move = False
user_move = (0, 0)

def await_move():
    global move_condition, needs_move, user_move
    needs_move = True
    with move_condition:
        move_condition.wait()
    needs_move = False
    return user_move

def set_game_state(new_game_state):
    global game_state
    game_state = new_game_state

def draw_player(screen: pygame.Surface, index: int, pos: tuple[int, int], size: int):
    x, y = pos

    if index == 0:
        hs = size // 2
        pygame.draw.line(screen, HL_COLOR, start_pos=(x - hs * 0.7, y - hs * 0.7), end_pos=(x + hs * 0.7, y + hs * 0.7), width=10)
        pygame.draw.line(screen, HL_COLOR, start_pos=(x - hs * 0.7, y + hs * 0.7), end_pos=(x + hs * 0.7, y - hs * 0.7), width=10)

    elif index == 1:
        pygame.draw.circle(screen, HL_COLOR, pos, radius=size * 0.35, width=7)

def draw_grid(screen: pygame.Surface):
    global game_state

    w, h = screen.get_size()
    cellw, cellh = w / 3, h / 3

    for i in range(3):
        for j in range(3):
            pygame.draw.rect(screen, HL_COLOR, rect=(i * cellw, j * cellh, cellw, cellh), width=2)
            if game_state.board[i][j] != -1:
                draw_player(screen, game_state.board[i][j], (i * cellw + cellw // 2, j * cellh + cellh // 2), min(cellw, cellh))

def visualize_ttt():
    global game_state, should_stop, move_condition, needs_move, user_move

    if game_state == None:
        raise Exception("No active game state")
    
    pygame.init()

    screen = pygame.display.set_mode(size=(400, 400))
    pygame.display.set_caption("Tic-Tac-Toe")

    while not should_stop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_stop = True
            
            elif event.type == pygame.MOUSEBUTTONDOWN and needs_move:
                w, h = screen.get_size()
                user_move = (int(event.pos[0] / w * 3), int(event.pos[1] / h * 3))
                with move_condition:
                    move_condition.notify()

        screen.fill(BG_COLOR)
        draw_grid(screen)
        pygame.display.flip()

    pygame.quit()
