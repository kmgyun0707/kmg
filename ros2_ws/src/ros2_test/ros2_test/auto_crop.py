import os
import cv2
import numpy as np
import glob

def order_points(pts):
    """
    4개의 좌표를 좌상단, 우상단, 우하단, 좌하단 순서로 정렬하는 함수.
    타일을 반듯하게 펴기 위해 반드시 필요함!
    """
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def main():
    # ==========================================
    # 📁 경로 설정 (내 환경에 맞게 수정 필수!)
    # ==========================================
    # 로보플로우에서 다운받은 데이터셋 경로
    images_dir = "roboflow_dataset/train/images"
    labels_dir = "roboflow_dataset/train/labels"
    
    # 크롭된 이미지가 저장될 Anomalib용 폴더 경로
    output_dir = "my_tile_dataset/train/good"
    os.makedirs(output_dir, exist_ok=True)

    # 이미지 파일 목록 불러오기 (jpg, png 등)
    image_paths = glob.glob(os.path.join(images_dir, "*.jpg"))
    crop_count = 0

    print("🚀 자동 크롭을 시작합니다...")

    for img_path in image_paths:
        # 이미지 읽기 및 크기 확인
        img = cv2.imread(img_path)
        if img is None:
            continue
        h, w = img.shape[:2]

        # 짝이 맞는 라벨(txt) 파일 찾기
        filename = os.path.basename(img_path)
        label_filename = os.path.splitext(filename)[0] + ".txt"
        label_path = os.path.join(labels_dir, label_filename)

        if not os.path.exists(label_path):
            continue # 라벨 파일이 없으면 패스

        # 라벨 파일 읽어서 처리
        with open(label_path, "r") as f:
            lines = f.readlines()

        for idx, line in enumerate(lines):
            data = line.strip().split()
            # YOLO OBB 포맷: class x1 y1 x2 y2 x3 y3 x4 y4
            if len(data) == 9: 
                class_id = data[0]
                
                # 0~1 사이로 정규화된 좌표를 실제 픽셀 좌표로 변환
                pts = np.array([
                    float(data[1]) * w, float(data[2]) * h,
                    float(data[3]) * w, float(data[4]) * h,
                    float(data[5]) * w, float(data[6]) * h,
                    float(data[7]) * w, float(data[8]) * h
                ]).reshape(4, 2)

                # 좌표 정렬 (좌상, 우상, 우하, 좌하)
                rect = order_points(pts)
                (tl, tr, br, bl) = rect

                # 변환할 새 이미지의 가로, 세로 길이 계산
                widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
                widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
                maxWidth = max(int(widthA), int(widthB))

                heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
                heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
                maxHeight = max(int(heightA), int(heightB))

                # 최종적으로 펴질 목적지 좌표
                dst = np.array([
                    [0, 0],
                    [maxWidth - 1, 0],
                    [maxWidth - 1, maxHeight - 1],
                    [0, maxHeight - 1]
                ], dtype="float32")

                # 변환 행렬(Perspective Transform) 계산 및 이미지 자르기
                M = cv2.getPerspectiveTransform(rect, dst)
                warped = cv2.warpPerspective(img, M, (maxWidth, maxHeight))

                # 크롭된 이미지 저장 (이름이 안 겹치게 원본이름_인덱스 부여)
                save_filename = f"{os.path.splitext(filename)[0]}_crop_{idx}.jpg"
                save_path = os.path.join(output_dir, save_filename)
                cv2.imwrite(save_path, warped)
                crop_count += 1

    print(f"✅ 총 {crop_count}개의 타일 이미지가 완벽하게 크롭되어 저장되었습니다!")

if __name__ == "__main__":
    main()