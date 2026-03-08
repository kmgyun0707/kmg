from ultralytics import YOLO

def main():
    print("🚀 YOLOv8 OBB 모델 학습을 시작합니다!")
    
    # 1. 회전 박스용(OBB) 가벼운 모델(nano)을 불러옵니다.
    # 처음 실행하면 인터넷에서 가중치 파일을 자동으로 다운로드합니다.
    model = YOLO('yolov8n-obb.pt')

    # 2. 본격적인 학습 시작!
    results = model.train(
        # ⭐ 아래 경로를 꼭! 압축 푸신 폴더 안의 data.yaml '절대 경로'로 적어주세요!
        data='/home/rokey/kmg/tile_dataset/data.yaml', 
        
        epochs=100,      # 문제집을 100번 반복해서 풉니다 (시간 없으면 50으로 줄여도 됩니다)
        imgsz=640,       # 로보플로우에서 설정했던 기본 이미지 사이즈
        device='cpu',      # '0'은 첫 번째 GPU를 쓰겠다는 뜻입니다. (GPU가 없거나 에러나면 'cpu'로 바꾸세요)
        batch=8          # 한 번에 볼 사진 장수. (그래픽카드 메모리가 부족해 뻗으면 4로 줄이세요)
    )
    
    print("✅ 학습이 완료되었습니다!")

if __name__ == '__main__':
    main()