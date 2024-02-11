import socket
import src.game as game

PORT = 4500
class NetworkException(Exception): pass

def host_address() -> str:
    return socket.gethostbyname(socket.gethostname())

def make_server() -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host_address(), PORT))
    server_socket.listen(1)
    return server_socket

def await_players(server_socket: socket.socket) -> list[socket.socket]:
    players = []
    for i in range(2):
        conn, addr = server_socket.accept()
        players.append(conn)
        print(f"Player {i + 1} joined the game (from: {addr[0]})")
    return players

def start_game(players: list[socket.socket]):
    game_state = game.GameState()

    conn1 = players[game_state.current_player]
    conn2 = players[1 - game_state.current_player]

    conn1.send("game-started:".encode("utf-8"))
    conn2.send("game-started:".encode("utf-8"))

    while game_state.move_available():
        conn1 = players[game_state.current_player]
        conn2 = players[1 - game_state.current_player]

        conn1.send("make-move:".encode("utf-8"))
        data = conn1.recv(1024).decode("utf-8").split(":")
        if data[0] != "my-move":
            raise NetworkException(f"Invalid response: '{data[0]}' to request: 'make-move'")
        conn2.send(f"other-made-move:{data[1]}".encode("utf-8"))
        
        xy = data[1].split(",")
        game_state.make_move(int(xy[0]), int(xy[1]))

        conn1.send(f"should-stop-game:".encode("utf-8"))
        should_stop1 = conn1.recv(1024).decode("utf-8").split(":")
        conn2.send(f"should-stop-game:".encode("utf-8"))
        should_stop2 = conn2.recv(1024).decode("utf-8").split(":")
        
        if should_stop1[1] == "yes" or should_stop2[1] == "yes":
            break
        
        winner = game_state.check_winner()
        if winner > -1:
            conn1.send(f"game-finnished:{winner}".encode("utf-8"))
            conn2.send(f"game-finnished:{winner}".encode("utf-8"))
            return

    winner = game_state.check_winner()
    conn1.send(f"game-finnished:{winner}".encode("utf-8"))
    conn2.send(f"game-finnished:{winner}".encode("utf-8"))