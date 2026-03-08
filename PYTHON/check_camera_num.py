import cv2

def find_working_cameras():
    print("🔍 연결된 카메라 번호를 찾고 있습니다. 잠시만 기다려주세요...")
    working_cams = []
    
    # 0번부터 9번까지 모든 인덱스를 다 테스트해 봅니다.
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✅ 빙고! {i}번 카메라가 정상 작동합니다! (해상도: {frame.shape[1]}x{frame.shape[0]})")
                working_cams.append(i)
            cap.release()
            
    if not working_cams:
        print("🚨 앗! 화면이 나오는 카메라를 하나도 찾지 못했습니다.")
        print("노트북 카메라가 물리적 스위치나 단축키(Fn)로 꺼져있는지 확인해 보세요!")
    else:
        print(f"👉 방금 찾은 번호({working_cams[0]})를 테스트 코드의 cv2.VideoCapture(번호) 에 넣고 다시 실행해 보세요!")

if __name__ == "__main__":
    find_working_cameras()