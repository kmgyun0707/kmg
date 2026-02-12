import cv2
import numpy as np

def analyze_real_photo(image_path):
    # 1. 이미지 읽기
    original_img = cv2.imread(image_path)
    if original_img is None:
        print("이미지를 찾을 수 없습니다!")
        return

    # 2. 관심 영역(ROI) 설정 (중요!)
    # 카메라가 타일 외에 책상이나 로봇 팔까지 찍을 수 있으므로,
    # 분석하고 싶은 '타일 부분'만 잘라냅니다. 
    # (실제 환경에 맞춰 좌표 수정 필요: y_start:y_end, x_start:x_end)
    # 예: 위에서 100~900픽셀, 왼쪽에서 200~1000픽셀만 사용
    roi_img = original_img[100:900, 200:1000] 
    
    # 만약 자르기 힘들면 그냥 원본 사용
    if roi_img.size == 0: roi_img = original_img 

    # 3. 전처리: 그레이스케일 변환 & 블러링
    gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
    
    # GaussianBlur: 자잘한 노이즈(먼지, 빛반사)를 뭉개서 없애줌
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 4. 이진화 (Thresholding) - 핵심!
    # "얼마나 밝아야 접착제로 볼 것인가?"를 결정합니다.
    # cv2.THRESH_OTSU: 컴퓨터가 알아서 최적의 임계값을 찾아주는 똑똑한 옵션입니다.
    # 배경이 검정, 접착제가 흰색이라고 가정합니다.
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 5. 형태학적 연산 (Morphology) - 구멍 메우기 (선택 사항)
    # 접착제 내부에 생긴 작은 기포나 끊김을 '접착된 것'으로 간주하여 메워줍니다.
    kernel = np.ones((5, 5), np.uint8)
    processed_binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # 6. 커버리지 계산
    total_pixels = processed_binary.size
    adhesive_pixels = cv2.countNonZero(processed_binary)
    coverage = (adhesive_pixels / total_pixels) * 100

    # 7. 결과 시각화 (눈으로 확인하기 위해)
    # 원본(ROI)에 접착제로 인식된 부분을 초록색으로 덧칠해서 보여줌
    display_img = roi_img.copy()
    # 이진화 이미지에서 흰색(255)인 부분만 초록색(0, 255, 0)으로 변경
    display_img[processed_binary == 255] = [0, 255, 0] 

    return coverage, display_img, processed_binary

# --- 실행 부분 ---
# 실제 찍은 사진 파일 경로를 넣으세요
image_file = "test_photo.jpg" 

# 테스트를 위해 임의의 파일이 없으면 에러가 나므로 예외처리
try:
    score, visual_result, binary_mask = analyze_real_photo(image_file)
    
    print(f"============ 분석 결과 ============")
    print(f"측정된 접착제 도포율(ECA): {score:.2f}%")
    
    if score >= 90.0:
        print("결과: ✅ 합격 (Pass)")
    else:
        print("결과: ❌ 불합격 (Fail) - 더 촘촘한 패턴이 필요합니다.")
        
    # 결과 창 띄우기
    cv2.imshow("Original (ROI)", visual_result) # 초록색으로 칠해진 결과
    cv2.imshow("Binary Mask", binary_mask)      # 흑백 마스크 (컴퓨터가 본 세상)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

except Exception as e:
    print(f"아직 사진 파일이 없어서 실행되지 않았습니다. ({e})")
    print("실제 사진을 찍어서 'test_photo.jpg'로 저장하고 다시 실행해보세요!")