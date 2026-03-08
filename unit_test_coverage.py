#흰색 접착제와 검은색 타일 바닥의 대비를 이용하여
#접착제 도포 품질을 검증하는 유닛 테스트 코드.

import cv2
import numpy as np



def create_mock_image(width=640, height=480, pattern_type='good'):
    """
    테스트를 위해 가상의 접착제 도포 이미지를 생성하는 함수
    pattern_type: 'good' (90% 이상), 'bad' (대충 바름)
    """
    # 1. 검은색 배경 생성 (타일 바닥)
    image = np.zeros((height, width), dtype=np.uint8)
    
    # 2. 하얀색으로 접착제 그리기 (시뮬레이션)
    if pattern_type == 'good':
        # 촘촘한 나선형/지그재그 패턴 (거의 꽉 참)
        cv2.rectangle(image, (50, 50), (width-50, height-50), 255, -1) 
        # 현실감을 위해 약간의 노이즈(빈 공간) 추가
        for _ in range(20):
            x = np.random.randint(50, width-50)
            y = np.random.randint(50, height-50)
            cv2.circle(image, (x, y), 10, 0, -1) # 검은 구멍 뚫기
            
    elif pattern_type == 'bad':
        # 대충 바른 패턴 (중간중간 빔)
        cv2.line(image, (50, 50), (width-50, height-50), 255, 20)
        cv2.line(image, (width-50, 50), (50, height-50), 255, 20)
        cv2.circle(image, (width//2, height//2), 50, 255, -1)

    return image

def analyze_coverage(image, threshold_percent=90.0):
    """
    이미지를 입력받아 커버리지(%)를 계산하고 합격 여부를 판단하는 함수
    """
    # 1. 전체 면적 (픽셀 수)
    total_area = image.shape[0] * image.shape[1]
    
    # 2. 접착제 면적 (흰색 픽셀 수, 0이 아닌 값)
    # 실제 사진에서는 이진화(Threshold) 과정이 필요하지만, 
    # Mock 이미지는 이미 흑백이므로 바로 카운트합니다.
    adhesive_area = cv2.countNonZero(image)
    
    # 3. 비율 계산
    coverage_ratio = (adhesive_area / total_area) * 100
    
    # 4. 결과 판단
    passed = coverage_ratio >= threshold_percent
    
    return coverage_ratio, passed

def main():
    print("=== 접착제 도포 품질 검증 Unit Test ===")
    
    # [시나리오 1] 잘 된 도포 케이스 테스트
    print("\n[Test 1] 우수 도포(Good) 케이스 검증 중...")
    img_good = create_mock_image(pattern_type='good')
    score, is_pass = analyze_coverage(img_good, threshold_percent=90.0)
    
    print(f" -> 측정된 커버리지: {score:.2f}%")
    if is_pass:
        print(" -> 결과: ✅ 합격 (PASS)")
    else:
        print(" -> 결과: ❌ 불합격 (FAIL)")
        
    # 결과 이미지 보여주기
    cv2.imshow("Test Case 1: Good", img_good)

    # [시나리오 2] 불량 도포 케이스 테스트
    print("\n[Test 2] 불량 도포(Bad) 케이스 검증 중...")
    img_bad = create_mock_image(pattern_type='bad')
    score, is_pass = analyze_coverage(img_bad, threshold_percent=90.0)
    
    print(f" -> 측정된 커버리지: {score:.2f}%")
    if is_pass:
        print(" -> 결과: ✅ 합격 (PASS)")
    else:
        print(" -> 결과: ❌ 불합격 (FAIL)") # 이게 정상
        
    # 결과 이미지 보여주기
    cv2.imshow("Test Case 2: Bad", img_bad)
    
    print("\n아무 키나 누르면 종료됩니다...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()