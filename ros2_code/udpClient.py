import socket

HOST = '127.0.0.1'  # 서버 주소
PORT = 12345            # 서버 포트

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_socket.sendto(b'Hello, UDP Server!', (HOST, PORT))

data, addr = client_socket.recvfrom(1024)
print(f"[UDP 클라이언트] {addr} 로부터 받은 메시지: {data.decode()}")

