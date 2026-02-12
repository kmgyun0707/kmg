import sys


def main():
    args = sys.argv[1:]  # 첫 번째 요소는 스크립트 이름이므로 제외
    sum = 0

    if len(args) > 0:
        for arg in args:
            sum = int(arg) + sum
            print(f"{arg}")
    else:
        print("No arguments were provided.")

    print(f'\nsum = {sum}\n')


if __name__ == "__main__":
    main()
