import socket
import threading
import os

def handle_client(client_socket):
    try:
        # Receive and decode username
        username = client_socket.recv(1024).decode('utf-8')
        print(username)
        user_dir = f'voice_messages/{username}'

        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        while True:
            # Receive and decode command
            command = client_socket.recv(1024).decode('utf-8')
            print(command)
            if command == 'SEND':
                recipient = client_socket.recv(1024).decode('utf-8')
                print(recipient)
                recipient_dir = f'voice_messages/{recipient}'

                if not os.path.exists(recipient_dir):
                    os.makedirs(recipient_dir)

                filename = client_socket.recv(1024).decode('utf-8')
                print(filename)
                file_size = int(client_socket.recv(1024).decode('utf-8'))
                print(file_size)

                with open(f'{recipient_dir}/{filename}', 'wb') as f:
                    received_size = 0
                    while received_size < file_size:
                        data = client_socket.recv(min(1024, file_size - received_size))
                        received_size += len(data)
                        f.write(data)

                client_socket.sendall('Voice message sent'.encode('utf-8'))

            elif command == 'RECEIVE':
                files = os.listdir(user_dir)
                files_list = ','.join(files)
                client_socket.sendall(files_list.encode('utf-8'))

                filename = client_socket.recv(1024).decode('utf-8')
                if filename in files:
                    file_size = os.path.getsize(f'{user_dir}/{filename}')
                    client_socket.sendall(str(file_size).encode('utf-8'))

                    with open(f'{user_dir}/{filename}', 'rb') as f:
                        while True:
                            data = f.read()
                            if not data:
                                break
                            client_socket.sendall(data)
                else:
                    client_socket.sendall('File not found'.encode('utf-8'))
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    print("Server listening on port 5555")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
