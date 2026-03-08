import cv2
import numpy as np

def main():
    # 🌟 찾으신 작동하는 카메라 번호로 변경하세요 (예: 0, 2, 4...)
    cap = cv2.VideoCapture(2) 

    if not cap.isOpened():
        print("🚨 웹캠을 열 수 없습니다.")
        return

    while True:
        ret, frame = cap.read()
        if not ret: break

        # 1. 흑백 변환 및 블러 (노이즈 제거)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # 2. 엣지 추출 (값 조정: 검은 타일이 잘 잡히도록 문턱값 낮춤)
        edges = cv2.Canny(blurred, 30, 100)
        
        # 선 끊김 보정
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        # 3. 외곽선 찾기
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # 면적이 너무 작은 쓰레기 데이터 무시 (화면 해상도에 따라 5000을 조절하세요)
            if area > 5000:
                # 🌟 핵심: 다각형 근사화 (도형의 꼭짓점 개수 파악)
                peri = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
                
                # 꼭짓점이 4개(사각형)일 때만 타일로 인정!
                if len(approx) == 4:
                    rect = cv2.minAreaRect(contour)
                    center, size, raw_angle = rect # 변수명을 angle에서 raw_angle로 살짝 바꿨습니다.

                    # 🚨 수정된 부분: 정사각형 타일 맞춤형 각도 보정 (-45도 ~ +45도)
                    # width, height를 비교해서 뒤집는 로직은 삭제합니다!
                    display_angle = raw_angle
                    
                    # OpenCV는 기본적으로 0~90도 사이를 줍니다.
                    # 45도를 넘어가면 90을 빼서 - 각도로 만들어줍니다.
                    if display_angle > 45.0:
                        display_angle -= 90.0

                    # 화면 시각화
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(frame, [box], 0, (0, 255, 0), 3) # 인식 성공 시 초록색 테두리
                    
                    text = f"Angle: {display_angle:.1f}"
                    cv2.putText(frame, text, (int(center[0])-50, int(center[1])), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow("Tile Rotation (Rectangle Filter)", frame)
        cv2.imshow("Debug Edges", closed)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()