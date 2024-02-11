# Alexander Hjort Fogh og August Leander Hedman
# alex453d@edu.nextkbh.dk, augu1789@edu.nextkbh.dk
# NEXT Sukkertoppen, S3n

import socket
import threading

import src.game as game
import src.visualize as visualize
from src.server import PORT

def make_player_client(host_addr: str) -> socket.socket:
    """Makes a socket and connects it to host_addr"""
    player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    player_socket.connect((host_addr, PORT))
    return player_socket

def start_game(player_socket: socket.socket) -> None:
    """Starts the pygame visualizer and communicates with the server"""
    game_state = game.GameState()
    visualize.set_game_state(game_state)

    # Start a second thread with the visualizer, since the recv()-function is blocking this thread
    visualizer_thread = threading.Thread(target=visualize.visualize_ttt)
    visualizer_thread.daemon = True
    visualizer_thread.start()

    while True:
        # Await message from server...
        data = player_socket.recv(1024).decode("utf-8")

        # ...this player should make a move
        if data == "make-move:":
            x, y = -1, -1
            if not visualize.should_stop:
                x, y = visualize.await_move()
            player_socket.send(f"my-move:{x},{y}".encode("utf-8"))
            game_state.make_move(x, y)
        
        # ...the other player made a move
        elif data.startswith("other-made-move:"):
            xy = data.split(":")[1].split(",")
            game_state.make_move(int(xy[0]), int(xy[1]))
        
        # ...should the server stop the game
        elif data == "should-stop-game:":
            should_stop = "yes" if visualize.should_stop else "no"
            player_socket.send(f"stop-game:{should_stop}".encode("utf-8"))

        # ...the server has stopped the game
        elif data.startswith("game-finnished:"):
            winner = data.split(":")[1]
            print(f"Game finnished!\nPlayer {winner} won!")

        # ...the server starts a new game
        elif data == "game-started:":
            game_state = game.GameState()
            visualize.set_game_state(game_state)

        # Check if server socket is closed
        elif data == "":
            break
    
    # Stop the visualizer
    visualize.should_stop = True
    visualizer_thread.join()
