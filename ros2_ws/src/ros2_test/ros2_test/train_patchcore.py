import os
from anomalib.data import Folder
from anomalib.models import Patchcore
from anomalib.engine import Engine

def main():
    print("🚀 PatchCore 이상탐지 모델 학습을 시작합니다...")

    # 1. 데이터셋 설정
    dataset_path = "./my_tile_dataset"
    
    # 🌟 수정된 부분: task 파라미터 삭제 (최신 Anomalib은 자동 인식함)
    datamodule = Folder(
        name="tile_dataset",
        root=dataset_path,
        normal_dir="train/good",
        abnormal_dir="test/defect", # 불량 테스트 데이터 폴더
        normal_test_dir="test/good" # 정상 테스트 데이터 폴더
    )
    datamodule.setup()

    # 2. 모델 설정 (가장 빠르고 가벼운 ResNet18 사용)
    model = Patchcore(backbone="resnet18", pre_trained=True)

    # 3. 학습 엔진 설정 및 실행
    # PatchCore는 가중치를 학습하는 게 아니라 특징을 메모리 뱅크에 저장하는 방식이라 1 에폭이면 끝!
    engine = Engine(task="classification", max_epochs=1)
    
    print("⏳ 데이터 특징(Feature) 추출 중... (금방 끝납니다!)")
    engine.fit(model=model, datamodule=datamodule)
    
    print("✅ 학습 완료! 결과물은 'results/' 폴더를 확인하세요.")

if __name__ == "__main__":
    main()