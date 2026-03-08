from ultralytics import YOLO
from datetime import datetime
import os

def main():
    # ★ 핵심: 이 파이썬 스크립트 파일이 위치한 폴더의 절대 경로를 가져옴
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
    
    # 스크립트가 이미 Fruits 폴더 안에 있다면 BASE_DIR이 곧 Fruits 폴더임
    OUTPUT_DIR = BASE_DIR 

    data_yaml_filename = "data.yaml"
    data_yaml_path = os.path.join(OUTPUT_DIR, data_yaml_filename)

    # 날짜/시간 기반 하위 폴더 이름 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    train_name = f"train_{timestamp}"
    val_name = f"val_{timestamp}"

    # Model 로드
    model = YOLO("yolov8n.pt")

    # Train 실행
    model.train(
        data=data_yaml_path,
        epochs=100,
        imgsz=640,
        batch=8,
        patience=20,
        project=OUTPUT_DIR,
        name=train_name
    )

    # Validation 실행 (학습된 best.pt 불러오기)
    best_model_path = os.path.join(OUTPUT_DIR, train_name, "weights", "best.pt")
    best_model = YOLO(best_model_path)
    
    best_model.val(
        data=data_yaml_path,
        project=OUTPUT_DIR,
        name=val_name
    )

    print(f"Train 결과:   {os.path.join(OUTPUT_DIR, train_name)}")
    print(f"Val 결과:     {os.path.join(OUTPUT_DIR, val_name)}")

if __name__ == '__main__':
    main()