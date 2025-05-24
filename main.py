import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import sounddevice as sd
import soundfile as sf
import socket
import threading
import os
import time

# Function to record a voice message
def record_voice(filename):
    fs = 44100  # Sample rate
    seconds = 5  # Duration of recording
    print("Recording...")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    sf.write(filename, myrecording, fs)
    print("Recording saved")

# Function to send a voice message to the server
def send_voice(username,client_socket):
    recipient = simpledialog.askstring("Recipient", "Enter recipient's username:")
    client_socket.send(username.encode('utf-8'))
    time.sleep(0.1)
    client_socket.send('SEND'.encode('utf-8'))
    time.sleep(0.1)
    client_socket.send(recipient.encode('utf-8'))
    time.sleep(0.1)

    filename = filedialog.askopenfilename()
    print(os.path.basename(filename))
    if not filename:
        return

    client_socket.send(os.path.basename(filename).encode('utf-8'))
    file_size = os.path.getsize(filename)
    client_socket.send(str(file_size).encode('utf-8'))
    time.sleep(0.1)
    with open(filename, 'rb') as f:
        data = f.read()
        client_socket.send(data)

    response = client_socket.recv(1024).decode('utf-8')
    messagebox.showinfo("Info", response)

    client_socket.close()

# Function to receive a voice message from the server
def receive_voice(username,client_socket):
    client_socket.send(username.encode('utf-8'))

    client_socket.send('RECEIVE'.encode('utf-8'))
    files_list = client_socket.recv(1024).decode('utf-8')
    files = files_list.split(',')

    selected_file = simpledialog.askstring("Select file", "Available files:\n" + "\n".join(files))
    client_socket.send(selected_file.encode('utf-8'))

    file_size = int(client_socket.recv(1024).decode('utf-8'))
    data = client_socket.recv(file_size)

    with open(f'received_{selected_file}', 'wb') as f:
        f.write(data)

    client_socket.close()
    messagebox.showinfo("Info", "Voice message received")

# Creating GUI
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))
    root = tk.Tk()
    root.title("Voice Mail Client")

    username = simpledialog.askstring("Username", "Enter your username:")

    record_button = tk.Button(root, text="Record Voice", command=lambda: record_voice("recorded_message.wav"))
    record_button.pack()

    send_button = tk.Button(root, text="Send Voice", command=lambda: send_voice(username,client_socket))
    send_button.pack()

    receive_button = tk.Button(root, text="Receive Voice", command=lambda: receive_voice(username,client_socket))
    receive_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
