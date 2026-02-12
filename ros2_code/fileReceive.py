import socket

# IPv4(AF_INET), TCP(SOCK_STREAM) 방식으로 서버 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 모든 IP(0.0.0.0)에서 오는 연결을 8080 포트에서 받음
server_socket.bind(('0.0.0.0', 8080))

# 클라이언트 연결을 최대 1개까지 대기(listen)
server_socket.listen(1)
print("서버가 시작되었습니다. 클라이언트를 기다리는 중...")

# 클라이언트 연결 요청 수락
connection, address = server_socket.accept()
print(f"클라이언트가 연결되었습니다: {address}")

# 수신한 파일을 저장할 파일을 바이너리 쓰기 모드(wb)로 오픈
with open('received_file.txt', 'wb') as file:
    print("파일 수신 시작...")

    # 클라이언트가 보내는 데이터를 1024byte씩 지속적으로 받음
    while True:
        data = connection.recv(1024)  # 1024바이트씩 수신
        if not data:  # 데이터가 더 이상 없으면 루프 종료
            break
        file.write(data)  # 수신한 데이터 조각을 파일에 기록
        print("파일 조각 수신 완료.")

# 연결 종료
connection.close()
server_socket.close()
