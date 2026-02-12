import sys


def main():
    args = sys.argv[1:]  # 첫 번째 요소는 스크립트 이름이므로 제외

    print(f"\nSource code is {sys.argv[0]}\n")

    if len(args) >= 2:
        print(f'{args[0]+ " " + args[1]}\n')

    else:
        print("No arguments were provided.")


if __name__ == "__main__":
    main()