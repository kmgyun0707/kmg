import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))
server_socket.listen(1)
print("서버가 시작되었습니다. 클라이언트를 기다리는 중...")

connection, address = server_socket.accept()
print(f"클라이언트가 연결되었습니다: {address}")

data = connection.recv(1024)
print(f"클라이언트로부터 받은 데이터: {data.decode()}")
connection.sendall(b'Hello, client!')

connection.close()
server_socket.close()
