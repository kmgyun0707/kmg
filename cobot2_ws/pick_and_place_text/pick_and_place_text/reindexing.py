import os
import glob

def main(args=None):
    # 사진이 저장된 폴더 경로 (현재 작업 환경에 맞게 수정)
    folder_path = "dataset/color"

    # 해당 폴더 안의 모든 jpg 파일을 찾아서 이름(예전 번호) 순으로 정렬
    files = sorted(glob.glob(os.path.join(folder_path, "*.jpg")))

    print(f"총 {len(files)}개의 파일 인덱스를 빈틈없이 당겨옵니다...")

    for new_index, old_filepath in enumerate(files):
        # 새로운 파일 이름 생성 (예: tile_0000.jpg)
        new_filename = f"tile_{new_index:04d}.jpg"
        new_filepath = os.path.join(folder_path, new_filename)
        
        # 예전 이름과 새 이름이 다를 때만 이름 변경
        if old_filepath != new_filepath:
            os.rename(old_filepath, new_filepath)

    print("✅ 깔끔하게 재정렬 완료되었습니다!")

if __name__ == '__main__':
    main()