import socket

def server_program():
    host = "0.0.0.0"  # 모든 인터페이스에서 수신
    port = 12345      # 사용할 포트 번호

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    

    print(f"Server is listening on {host}:{port} ...")

    conn, address = server_socket.accept()
    print(f"Connection from: {address}")

    while True:
        client_message = conn.recv(1024).decode()
        if client_message.lower() == 'bye':
            print("Connection closed by the client.")
            break   
        print(f"Message from client: {client_message}")
        
        server_message = input("You: ")
        conn.send(server_message.encode())
        if server_message.lower() == 'bye':
            print("Connection closed by the server.")
            break

    conn.close()
    server_socket.close()

if __name__ == '__main__':
    server_program()
        