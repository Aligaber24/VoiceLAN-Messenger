import socket
import threading

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Received from server: {message.decode('utf-8')}")
        except:
            break

# Main client function
def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5000))

    # Start a new thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Send username
    username = input("Enter username: ")
    client_socket.send(username.encode('utf-8'))

    # Send password
    password = input("Enter password: ")
    client_socket.send(password.encode('utf-8'))

    # Wait for some time to receive the server response before closing the socket
    receive_thread.join(timeout=2)
    client_socket.close()

if __name__ == "__main__":
    client_program()
