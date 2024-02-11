import socket
import src.game as game
from src.server import PORT, NetworkException
from random import randint

def make_player_client(host_addr: str) -> socket.socket:
    player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    player_socket.connect((host_addr, PORT))
    return player_socket

def start_game(player_socket: socket.socket) -> None:
    game_state = game.GameState()

    while True:
        data = player_socket.recv(1024).decode("utf-8")
        print(data)

        if data == "make-move:":
            for i in range(3):
                print("| ", end="")
                for j in range(3):
                    player = game_state.board[i][j]
                    print(["x", "o", " "][player], end="")
                print(" |")
            
            x, y = randint(0, 2), randint(0, 2) # https://docs.python.org/3/library/threading.html#threading.Condition.wait
            player_socket.send(f"my-move:{x},{y}".encode("utf-8"))
            game_state.make_move(x, y)
        
        elif data.startswith("other-made-move:"):
            xy = data.split(":")[1].split(",")
            game_state.make_move(int(xy[0]), int(xy[1]))
        
        elif data == "should-stop-game:":
            player_socket.send(f"stop-game:no".encode("utf-8"))

        elif data.startswith("game-finnished:"):
            winner = data.split(":")[1]
            print(f"Game finnished!\nPlayer {winner} won!")

        elif data == "game-started:":
            game_state = game.GameState()

        elif data == "":
            break
