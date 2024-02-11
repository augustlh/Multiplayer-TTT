# Alexander Hjort Fogh og August Leander Hedman
# alex453d@edu.nextkbh.dk, augu1789@edu.nextkbh.dk
# NEXT Sukkertoppen, S3n

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
    """Awaits a move from the user and retrieves it. Blocks the main thread."""
    global move_condition, needs_move, user_move
    needs_move = True
    with move_condition:
        move_condition.wait()
    needs_move = False
    return user_move

def set_game_state(new_game_state):
    """Sets the game state"""
    global game_state
    game_state = new_game_state

def draw_player(screen: pygame.Surface, index: int, pos: tuple[int, int], size: int):
    """Draws a player at the given position on the screen/game board. 
    index is the state of the given cell on the grid: 0 for X, 1 for O, -1 for empty."""
    x, y = pos

    # Draws the player as an X (with lines) if index is 0, as a circle if index is 1
    if index == 0:
        hs = size // 2
        pygame.draw.line(screen, HL_COLOR, start_pos=(x - hs * 0.7, y - hs * 0.7), end_pos=(x + hs * 0.7, y + hs * 0.7), width=10)
        pygame.draw.line(screen, HL_COLOR, start_pos=(x - hs * 0.7, y + hs * 0.7), end_pos=(x + hs * 0.7, y - hs * 0.7), width=10)

    elif index == 1:
        pygame.draw.circle(screen, HL_COLOR, pos, radius=size * 0.35, width=7)

def draw_grid(screen: pygame.Surface):
    """Draws the game grid/state on the screen"""
    global game_state

    w, h = screen.get_size()
    cellw, cellh = w / 3, h / 3

    for i in range(3):
        for j in range(3):
            # Draws the game board as a grid of rectangles
            pygame.draw.rect(screen, HL_COLOR, rect=(i * cellw, j * cellh, cellw, cellh), width=2)
            # If a cell in the game_board has a different state from empty/draw it draws the player/value of game_state.board[i][j]
            if game_state.board[i][j] != -1:
                draw_player(screen, game_state.board[i][j], (i * cellw + cellw // 2, j * cellh + cellh // 2), min(cellw, cellh))

def visualize_ttt():
    """Initializes a pygame window to visualize a Tic-Tac-Toe game based on the game_state."""
    global game_state, should_stop, move_condition, needs_move, user_move

    if game_state == None:
        raise Exception("No active game state")
    
    # Initializes pygame
    pygame.init()

    screen = pygame.display.set_mode(size=(400, 400))
    pygame.display.set_caption("Tic-Tac-Toe")

    # Main loop
    while not should_stop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_stop = True
            
            # If the user clicks on the screen and its their turn, notify the main thread
            elif event.type == pygame.MOUSEBUTTONDOWN and needs_move:
                w, h = screen.get_size()
                user_move = (int(event.pos[0] / w * 3), int(event.pos[1] / h * 3))
                with move_condition:
                    move_condition.notify()

        # Draws the game state
        screen.fill(BG_COLOR)
        draw_grid(screen)
        pygame.display.flip()

    pygame.quit()
