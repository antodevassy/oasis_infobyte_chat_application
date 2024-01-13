import socket
import threading

# Server configuration
HOST = "127.0.0.1"
PORT = 55555

# Dictionary to store client connections and usernames
clients = {}


def handle_client(client_socket, username):
    try:
        while True:
            message = client_socket.recv(1024).decode("utf-8")
            if message == "/exit":
                break

            broadcast(f"{username}: {message}")

    except ConnectionResetError:
        print(f"Connection with {username} closed.")
    finally:
        remove_client(username, client_socket)


def broadcast(message):
    for client_socket in clients:
        try:
            client_socket.send(message.encode("utf-8"))
        except BrokenPipeError:
            continue


def remove_client(username, client_socket):
    del clients[client_socket]
    print(f"{username} has left the chat.")
    broadcast(f"{username} has left the chat.")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            username = client_socket.recv(1024).decode("utf-8")
            print(f"{username} connected from {addr}")

            clients[client_socket] = username
            broadcast(f"{username} has joined the chat.")

            # Handle each client in a separate thread
            client_handler = threading.Thread(target=handle_client, args=(client_socket, username))
            client_handler.start()

    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
