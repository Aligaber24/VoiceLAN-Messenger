import socket
import threading


# Function to handle client connections
def handle_client(client_socket):
    try:
        # Receive username
        username = client_socket.recv(1024).decode('utf-8')
        print(f"Received username: {username}")

        # Receive password
        password = client_socket.recv(1024).decode('utf-8')
        print(f"Received password: {password}")

        # Respond to client
        client_socket.send("Credentials received".encode('utf-8'))

        # You can add further processing here
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


# Main server function
def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(5)
    print("Server started on port 5000")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        # Start a new thread to handle the client connection
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    server_program()
