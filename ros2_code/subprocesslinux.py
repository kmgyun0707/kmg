import subprocess

# 디렉토리 목록 출력 함수 (Linux)
def dir():
    # 'ls -l' 명령을 실행하고 결과를 문자열로 가져옴
    result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
    print("Output of 'dir' command:")
    print(result.stdout)  # 명령 출력 내용 표시

# 계산기 실행 함수 (Linux: GNOME Calculator)
def calculator():
    # gnome-calculator 실행
    result = subprocess.run(['gnome-calculator'], capture_output=True, text=True)
    print("Output of 'calculator' command:")
    print(result.stdout)  # GUI 프로그램은 일반적으로 출력 없음

# Visual Studio Code 실행 함수
def vscode():
    # 'code' 명령어로 VS Code 실행
    result = subprocess.run(['code'], capture_output=True, text=True)
    print("Output of 'vscode' command:")
    print(result.stdout)  # 출력 내용이 있다면 표시

# 메인 실행 영역
if __name__ == "__main__":
    dir()         # 현재 디렉토리 목록 출력
    calculator()  # 계산기 실행
    vscode()      # VS Code 실행
