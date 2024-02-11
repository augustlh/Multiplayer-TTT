# Alexander Hjort Fogh og August Leander Hedman
# alex453d@edu.nextkbh.dk, augu1789@edu.nextkbh.dk
# NEXT Sukkertoppen, S3n

class GameState:
    def __init__(self) -> None:
        """GameState represents a game of Tic-Tac-Toe"""
        self.current_player = 0
        self.board = [[-1 for _ in range(3)] for _ in range(3)]

    def check_winner(self) -> int:
        """Check all diagonals, rows, and columns for a winning combination"""
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2]:
                return self.board[i][0]
        
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i]:
                return self.board[0][i]
        
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[0][0]
        
        if self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return self.board[0][2]
        
        # In case of no combinations, return -1 (draw)
        return -1

    def move_available(self):
        """Checks if a cell is available"""
        return -1 in self.board[0] + self.board[1] + self.board[2]
    
    def make_move(self, x: int, y: int) -> None:
        """Makes a move and updates the current player"""
        self.board[x][y] = self.current_player
        self.current_player = 1 - self.current_player
