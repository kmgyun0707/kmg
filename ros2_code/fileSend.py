import socket

# IPv4(AF_INET), TCP(SOCK_STREAM) 방식으로 클라이언트 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결 (IP: 127.0.0.1, PORT: 8080)
client_socket.connect(("127.0.0.1", 8080))
print("서버에 연결되었습니다.")

# 보낼 파일을 이진 모드(rb)로 열기
with open("sendfile.txt", "rb") as file:
    print("파일 전송 시작...")

    # 파일을 1024바이트씩 나누어 전송
    while True:
        data = file.read(1024)  # 1024바이트 단위로 읽기
        if not data:           # 더 이상 읽을 내용이 없으면 종료
            break

        client_socket.sendall(data)  # 서버로 데이터(파일 조각) 전송

    print("파일 조각 전송 완료.")

# 파일 전송이 끝나면 소켓 닫기
client_socket.close()
