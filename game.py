import pygame

class GameState:
    def player_made_move():
        pass

class Board:
    def __init__(self, rows, cols):
        self.rows, self.cols = rows, cols
        self.grid = [[0 for _ in range(rows)] for _ in range(cols)]

    def check_winner() -> int:
        """Check all diagonals, rows, and columns"""
        pass

# game gøj

#move
# yo player x lav et move
# server siger til player x, lav et move
# player laver et move og siger det til server, som fortæller det til spiller y
# ... repeat med spiller y
    
# n - current_spiller