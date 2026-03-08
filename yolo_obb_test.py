import cv2
from ultralytics import YOLO
import numpy as np

def main():
    # 1. 🌟 학습한 모델(best.pt)의 '절대 경로'를 입력하세요!
    model_path = '/home/rokey/kmg/yolov26n_obb.pt'
    try:
        model = YOLO(model_path)
        print(f"✅ 모델 로드 성공: {model_path}")
    except Exception as e:
        print(f"🚨 모델 로드 실패: {e}")
        return

    # 2. 🌟 작동하는 카메라 번호로 변경하세요 (예: 0, 2, 4...)
    cap = cv2.VideoCapture(4) 

    if not cap.isOpened():
        print("🚨 웹캠을 열 수 없습니다.")
        return

    print("📷 YOLOv26 OBB 실시간 검증을 시작합니다. 'q' 키를 누르면 종료됩니다.")

    while True:
        ret, frame = cap.read()
        if not ret: break

        # 3. YOLO OBB 추론 수행
        # verbose=False로 설정하면 터미널이 로그로 도배되는 것을 막습니다.
        results = model(frame, verbose=False)

        # 4. 🌟 OBB 시각화의 핵심!
        # results[0].plot() 함수는 회전 박스, 클래스 이름, 신뢰도(conf)가 
        # 예쁘게 그려진 이미지를 직접 반환합니다.
        annotated_frame = results[0].plot()

        # 5. 각도 데이터 추출 및 터미널 출력 (디버깅용)
        # 탐지된 객체가 있을 때만 실행
        if results[0].obb:
            for i, obb in enumerate(results[0].obb):
                # .xywhr 속성에서 [중심x, 중심y, 너비, 높이, 라디안 각도]를 가져옵니다.
                _, _, _, _, angle_rad = obb.xywhr[0].cpu().numpy()
                confidence = obb.conf[0].cpu().numpy()
                
                # 라디안을 각도(degree)로 변환 (-180 ~ 180도 사이 값)
                angle_deg = np.degrees(angle_rad)
                
                # 사람이 보기 편한 -45 ~ +45도 범위로 보정 (정사각형 타일 기준)
                display_angle = angle_deg
                if display_angle > 45:
                    display_angle -= 90
                elif display_angle < -45:
                    display_angle += 90

                # 시각화 화면 왼쪽에 각도 글씨 쓰기
                text = f"Tile #{i}: {display_angle:.1f}deg (Conf: {confidence:.2f})"
                cv2.putText(annotated_frame, text, (10, 30 + (i*30)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # 6. 화면 출력
        cv2.imshow("YOLOv8 OBB Real-time Verification", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()