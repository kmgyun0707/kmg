import sys


def main():
    args = sys.argv[1:]  # 첫 번째 요소는 스크립트 이름이므로 제외
    items = ""

    print(f"\nSource code is {sys.argv[0]}\n")

    if len(args) >= 2:
        for item in args:
            items += item
            items += " "
            print(f"{items}\n")
    else:
        print("No arguments were provided.")


if __name__ == "__main__":
    main()
