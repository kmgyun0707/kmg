import cv2
import numpy as np

def analyze_real_photo(image_path, label_text="Image"):
    # 1. 이미지 읽기
    original_img = cv2.imread(image_path) # 이미지 파일 경로를 입력받아 읽어옴
    if original_img is None:
        print(f"Error: '{image_path}' 이미지를 찾을 수 없습니다!")
        return None, None

    # 2. 이미지 크기 통일 (비교를 위해 필수)
    # 두 사진의 해상도가 다를 수 있으므로 640x640(또는 원하는 크기)으로 리사이징
    target_size = (640, 640) 
    original_img = cv2.resize(original_img, target_size)

    # 3. 관심 영역(ROI) 설정
    # 테두리나 배경 노이즈를 피하기 위해 가장자리 20픽셀씩 잘라냄 (필요 시 조절)
    h, w = original_img.shape[:2]
    roi_img = original_img[20:h-20, 20:w-20] 

    # 4. 전처리: 그레이스케일 & 블러링
    gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 5. 이진화 (Thresholding)
    # 보내주신 사진은 '검은색 펜'이 접착제이므로, THRESH_BINARY_INV(반전)를 사용해야 함.
    # 배경(흰색) -> 0(검정), 접착제(검은색) -> 255(흰색)으로 변환
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 6. 형태학적 연산 (노이즈 제거 및 구멍 메우기)
    kernel = np.ones((3, 3), np.uint8)
    processed_binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel) # 노이즈 제거
    processed_binary = cv2.morphologyEx(processed_binary, cv2.MORPH_CLOSE, kernel) # 끊김 연결

    # 7. 커버리지 계산
    total_pixels = processed_binary.size # ROI 영역의 총 픽셀 수
    adhesive_pixels = cv2.countNonZero(processed_binary) # 접착제(흰색) 픽셀 수
    coverage = (adhesive_pixels / total_pixels) * 100 # 백분율로 계산

    # 8. 결과 시각화
    # 원본(ROI)에 초록색 덧칠
    display_img = roi_img.copy()
    display_img[processed_binary == 255] = [0, 255, 0] # 접착제 부분을 초록색으로

    # 결과 텍스트 이미지 위에 적기
    cv2.putText(display_img, f"{label_text}: {coverage:.1f}%", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    return coverage, display_img

# --- 실행 부분 ---

# 1. 비교할 두 이미지 파일명 입력 (보내주신 파일명 예시)
file_1 = "/home/rokey/kmg/test_img/12.png"     # 첫 번째 사진
file_2 = "/home/rokey/kmg/test_img/13.png" # 두 번째 사진

print("=== 접착제 도포 비교 분석 시작 ===")

try:
    # 2. 각각 분석 수행
    score1, result1 = analyze_real_photo(file_1, "Method A")
    score2, result2 = analyze_real_photo(file_2, "Method B")

    if result1 is not None and result2 is not None:
        # 3. 콘솔 결과 출력
        print(f"\n[분석 결과]")
        print(f"이미지 1 (Method A): {score1:.2f}%")
        print(f"이미지 2 (Method B): {score2:.2f}%")
        
        diff = score2 - score1
        print(f"-> 차이: {abs(diff):.2f}% 포인트 ({'증가' if diff > 0 else '감소'})")

        # 4. 이미지 가로로 붙이기 (Stacking)
        # 결과 이미지를 나란히 붙여서 한 창에 띄움
        final_view = np.hstack((result1, result2))

        cv2.imshow("Comparison: Method A vs Method B", final_view)
        print("\n결과 창이 열렸습니다. 아무 키나 누르면 종료됩니다.")
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("이미지 처리에 실패했습니다. 파일 경로를 확인해주세요.")

except Exception as e:
    print(f"에러 발생: {e}")