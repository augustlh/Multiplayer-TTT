
class GameState:
    def __init__(self) -> None:
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
        
        return -1

    def move_available(self):
        return -1 in self.board[0] + self.board[1] + self.board[2]
    
    def make_move(self, x: int, y: int) -> None:
        self.board[x][y] = self.current_player
        self.current_player = 1 - self.current_player
