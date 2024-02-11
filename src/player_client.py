import socket
import threading
from random import randint

import src.game as game
import src.visualize as visualize
from src.server import PORT, NetworkException

def make_player_client(host_addr: str) -> socket.socket:
    player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    player_socket.connect((host_addr, PORT))
    return player_socket

def start_game(player_socket: socket.socket) -> None:
    game_state = game.GameState()
    visualize.set_game_state(game_state)

    visualizer_thread = threading.Thread(target=visualize.visualize_ttt)
    visualizer_thread.daemon = True
    visualizer_thread.start()

    while True:
        data = player_socket.recv(1024).decode("utf-8")
        # print(data)

        if data == "make-move:":
            x, y = -1, -1
            if not visualize.should_stop:
                x, y = visualize.await_move()
            player_socket.send(f"my-move:{x},{y}".encode("utf-8"))
            game_state.make_move(x, y)
        
        elif data.startswith("other-made-move:"):
            xy = data.split(":")[1].split(",")
            game_state.make_move(int(xy[0]), int(xy[1]))
        
        elif data == "should-stop-game:":
            should_stop = "yes" if visualize.should_stop else "no"
            player_socket.send(f"stop-game:{should_stop}".encode("utf-8"))

        elif data.startswith("game-finnished:"):
            winner = data.split(":")[1]
            print(f"Game finnished!\nPlayer {winner} won!")

        elif data == "game-started:":
            game_state = game.GameState()
            visualize.set_game_state(game_state)

        elif data == "":
            break
    
    visualizer_thread.join()
