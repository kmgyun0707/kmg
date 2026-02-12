import socket

HOST = '0.0.0.0'  # 모든 인터페이스에서 수신
PORT = 12345      # 사용할 포트 번호

# UDP 서버 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))    

print(f"[UDP 서버] {HOST}:{PORT} 에서 메시지 수신 대기 중...")

data, addr = server_socket.recvfrom(1024)
print(f"[UDP 서버] {addr} 로부터 받은 메시지: {data.decode()}") 

server_socket.sendto(b'Hello, UDP client!', addr)