# Alexander Hjort Fogh og August Leander Hedman
# alex453d@edu.nextkbh.dk, augu1789@edu.nextkbh.dk
# NEXT Sukkertoppen, S3n

import socket
import src.game as game

PORT = 4500
class NetworkException(Exception): pass

def host_address() -> str:
    """Returns the host's IP address"""
    return socket.gethostbyname(socket.gethostname())

def make_server() -> socket.socket:
    """Creates a server socket and binds it to the host's IP address and the PORT"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host_address(), PORT))
    server_socket.listen(1)
    return server_socket

def await_players(server_socket: socket.socket) -> list[socket.socket]:
    """Awaits two players to join the game and returns their sockets in a list"""
    players = []
    for i in range(2):
        conn, addr = server_socket.accept()
        players.append(conn)
        print(f"Player {i + 1} joined the game (from: {addr[0]})")
    return players

def start_game(players: list[socket.socket]):
    """Starts a new game of Tic-Tac-Toe on the server"""
    game_state = game.GameState()

    # The two player sockets
    conn1 = players[game_state.current_player]
    conn2 = players[1 - game_state.current_player]

    # Communicate that a new game has started
    conn1.send("game-started:".encode("utf-8"))
    conn2.send("game-started:".encode("utf-8"))

    while game_state.move_available():
        conn1 = players[game_state.current_player]
        conn2 = players[1 - game_state.current_player]

        # Ask the first player to make a move...
        conn1.send("make-move:".encode("utf-8"))
        data = conn1.recv(1024).decode("utf-8").split(":")
        if data[0] != "my-move":
            raise NetworkException(f"Invalid response: '{data[0]}' to request: 'make-move'")
        # ...and communicate the move to the other player
        conn2.send(f"other-made-move:{data[1]}".encode("utf-8"))
        
        # Retrive the x and y index from de message
        xy = data[1].split(",")
        if int(xy[0]) < 0 or int(xy[1]) < 0:
            break
        game_state.make_move(int(xy[0]), int(xy[1]))

        # Check with both players if game should stop
        conn1.send(f"should-stop-game:".encode("utf-8"))
        should_stop1 = conn1.recv(1024).decode("utf-8").split(":")
        conn2.send(f"should-stop-game:".encode("utf-8"))
        should_stop2 = conn2.recv(1024).decode("utf-8").split(":")
        
        if should_stop1[1] == "yes" or should_stop2[1] == "yes":
            break
        
        # Check if a player has won
        winner = game_state.check_winner()
        if winner > -1:
            conn1.send(f"game-finnished:{winner}".encode("utf-8"))
            conn2.send(f"game-finnished:{winner}".encode("utf-8"))
            return

    # Communicate that the game has ended
    winner = game_state.check_winner()
    conn1.send(f"game-finnished:{winner}".encode("utf-8"))
    conn2.send(f"game-finnished:{winner}".encode("utf-8"))
