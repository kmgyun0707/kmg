import socket
import sys


def client_program():
    host = "127,0,0,1"  # 서버 주소
    port = 12345  # 서버 포트

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print(f"Connected to server at {host}:{port}")

    while True:
        client_message = input("Enter message to send (type 'bye' to quit): ")
        client_socket.send(client_message.encode())
        if client_message.lower() == "bye":
            print("Connection closed by the client.")
            break

        server_message = client_socket.recv(1024).decode()
        if server_message.lower() == "bye":
            print("Connection closed by the server.")
            break

        print(f"Server : {server_message}")

    client_socket.close()


if __name__ == "__main__":
    client_program()
