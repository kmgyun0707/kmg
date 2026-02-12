import subprocess

# # 디렉토리 목록 출력 함수(현재는 사용하지 않음)
# def dir():
#     # 'ls -l' 명령을 실행하고 결과를 받아옴 (Linux 명령)
#     result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
#     print("Output of 'dir' command:")
#     print(result.stdout)


# ipconfig 명령 실행: 윈도우의 네트워크 설정 정보를 출력
def ipconfig():
    result = subprocess.run(["ipconfig"], capture_output=True, text=True)
    print("Output of 'ipconfig' command:")
    print(result.stdout)


# 메모장 실행 함수
def notepad():
    # notepad.exe 실행 (capture_output=False 기본값 → 출력 없음)
    result = subprocess.run(["notepad.exe"])
    print("Output of Notepad command:")
    print(result.stdout)


# 그림판(paint) 실행 함수
def pbrush():
    # pbrush.exe 실행
    result = subprocess.run(["pbrush.exe"])
    print("Output of 'pbrush' command:")
    print(result.stdout)


# 계산기 실행 함수
def calc():
    # calc.exe 실행
    result = subprocess.run(["calc.exe"])
    print("Output of 'calc' command:")
    print(result.stdout)


# 메인 실행 영역
if __name__ == "__main__":
    # dir()  # 디렉토리 출력 함수는 현재 주석 처리됨
    ipconfig()   # ipconfig 실행
    notepad()    # 메모장 실행
    pbrush()     # 그림판 실행
    calc()       # 계산기 실행
