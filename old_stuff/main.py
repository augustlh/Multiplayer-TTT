import pygame
import sys
import socket

class Board:
    def __init__(self, rows : int, cols : int) -> None:
        self.grid = [[0 for _ in range(rows)] for _ in range(cols)]

    def check_win(self):
        pass

class View:
    def __init__(self, rows : int, cols : int) -> None:
        self.rows = rows
        self.cols = cols
        self.colors = [(255,0,0), (255,255,0), (0, 255, 255), (0, 255, 0), (0, 0, 255)]

        # Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((400,400))
        pygame.display.set_caption("Kryds og Bolle")
        self.size = self.screen.get_width() // rows
        self.screen.fill((255,255,255))
        # clock = pygame.time.Clock()

    def draw_board(self, board : Board):
        for i in range(self.rows):
            for j in range(self.cols):
                pygame.draw.rect(self.screen, (0,0,0), (i*self.size, j*self.size, self.size, self.size), 1)
                if board.grid[i][j] != 0: pygame.draw.circle(self.screen, self.colors[board.grid[i][j]], (i*self.size + self.size / 2, j*self.size + self.size / 2), self.size * 0.2)

    def update(self):
        pygame.display.flip()

class Controller:
    def __init__(self, board : Board, view : View) -> None:
        self.board = board
        self.view = view

    def start_game(self):
        pass

    def get_input(self, player):
        #connection = playerConnections[player]
        pass

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            #ændrer til mouseclick og server logik senere
            if 1 == 1:
                if self.board.check_win():
                    print("En gut har vundet")
                    pygame.quit()
                    sys.exit(0)

serverSocket = socket.socket()
host = socket.gethostbyname(socket.gethostname())
port = 8080


connections = []
addresses = []

def start_server():
    try:
        serverSocket.bind((host, port))
        print("Server started. Binding to port", port)
        serverSocket.listen(1)

        for _ in range(2):
            connection, address = serverSocket.accept()
            print(connection, address, "\n", type(connection), type(address))

            connections.append(connection)
            addresses.append(address)


    except socket.error as error:
        print("Error:", error)

start_server()

data = connections[0].recv(1024).decode("utf-8")
print(data)

#rows, cols = 3,3 
#board = Board(rows, cols)
#view = View(rows, cols)
#controller = Controller(board, view)

#while True:
#    controller.event_handler()
#    view.draw_board(board)
#    view.update()

