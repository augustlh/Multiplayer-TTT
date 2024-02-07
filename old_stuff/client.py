import socket

try:
    host_ip = socket.gethostbyname(socket.gethostname())
    port = 8080

    client_socket = socket.socket()
    client_socket.connect((host_ip, port))

    data = "-_-"
    client_socket.send(data.encode())

    # Additional code for receiving data, if necessary

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client_socket.close()
