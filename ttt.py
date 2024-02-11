import sys
import re
import src.server as server
import src.player_client as client

# Check number of arguments
if len(sys.argv) < 2:
    print(f"Invalid usage \nUse: {sys.argv[0]} server|connect [address]")
    sys.exit(-1)

# Create new server, and start game
if sys.argv[1] == "server":
    print(f"Creating server at {server.host_address()}...")

    try:
        server_socket = server.make_server()
        players = server.await_players(server_socket)

        while True:
            server.start_game(players)
            response = input("Start new game [y/N]? ")
            if response.lower() != "y":
                break
            players[0], players[1] = players[1], players[0]
    
    except server.NetworkException as e:
        print(e)
        
    finally:
        server_socket.close()

# Connect to server, and open game window
elif sys.argv[1] == "connect":
    if len(sys.argv) < 3:
        print("No host address provided\nPlease specify address in format: '0.0.0.0'")
        sys.exit(-1)
    
    if not re.fullmatch("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", sys.argv[2]):
        print("Invalid address format\nPlease specify address in format: '0.0.0.0'")
        sys.exit(-1)
    
    print(f"Connecting to server at {sys.argv[2]}...")
    player_socket = client.make_player_client(sys.argv[2])
    client.start_game(player_socket)
    player_socket.close()

# Invalid first argument
else:
    print(f"Invalid argument: '{sys.argv[1]}'\nPlease provide either 'server' to create a new server, or 'connect' to connect to a server")
    sys.exit(-1)
