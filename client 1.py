import socket
import threading

# Server configuration
HOST = "127.0.0.1"
PORT = 55555

# Function to receive and display messages from the server
def receive_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode("utf-8")
            print(message)
    except ConnectionResetError:
        print("Connection with the server closed.")
        exit()


def main():
    username = input("Enter your username: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.send(username.encode("utf-8"))

    # Start a thread to receive and display messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    try:
        while True:
            message = input()
            client_socket.send(message.encode("utf-8"))

            if message == "/exit":
                break

    except KeyboardInterrupt:
        pass
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
