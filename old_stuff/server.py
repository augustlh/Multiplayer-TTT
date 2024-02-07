import socket

def start_server():
    host = '127.0.0.1'  # localhost
    port = 12345         # Port to bind to

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        # Accept a connection from a client
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received data: {data}")

        # Check if the client wants to exit
        if data.lower() == 'exit':
            print("Server is closing...")
            break

        # Echo the data back to the client
        client_socket.sendall(data.encode('utf-8'))

        # Close the connection
        client_socket.close()

    # Close the server socket
    server_socket.close()
    print("Server closed")

if __name__ == "__main__":
    start_server()