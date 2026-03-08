# 카메라에서 컬러 이미지를 수신하여 OpenCV 창에 표시하고, 사용자가 's' 키 또는 스페이스바를 눌러 사진을 저장할 수 있는 ROS2 노드입니다.
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
import cv2
import os

# 1. 카메라 노드 클래스
class ImgNode(Node):
    def __init__(self):
        super().__init__('img_node')
        self.bridge = CvBridge()
        self.color_frame = None
        self.color_frame_stamp = None
        self.depth_frame = None
        self.intrinsics = None
        self.color_subscription = self.create_subscription(
            Image, '/camera/camera/color/image_raw', self.color_callback, 10)
        self.depth_subscription = self.create_subscription(
            Image, '/camera/camera/aligned_depth_to_color/image_raw', self.depth_callback, 10)
        self.camera_info_subscription = self.create_subscription(
            CameraInfo, '/camera/camera/color/camera_info', self.camera_info_callback, 10)
        self.get_logger().info("Waiting for client's call...")

    def camera_info_callback(self, msg):
        self.intrinsics = {"fx": msg.k[0], "fy": msg.k[4], "ppx": msg.k[2], "ppy": msg.k[5]}

    def color_callback(self, msg):
        self.color_frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self.color_frame_stamp = str(msg.header.stamp.sec) + str(msg.header.stamp.nanosec)

    def depth_callback(self, msg):
        self.depth_frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

    def get_color_frame(self):
        return self.color_frame

    def get_color_frame_stamp(self):
        return self.color_frame_stamp

    def get_depth_frame(self):
        return self.depth_frame

    def get_camera_intrinsic(self):
        return self.intrinsics


# ==========================================
# 2. 사진 촬영 메인 함수 (뎁스 저장 제거)
# ==========================================
def main(args=None):
    rclpy.init(args=args)
    node = ImgNode()

    # 컬러 사진을 저장할 폴더만 생성
    save_dir_color = "dataset/color"
    os.makedirs(save_dir_color, exist_ok=True)

    img_count = 0 # 사진 번호 카운터

    cv2.namedWindow("Camera View", cv2.WINDOW_AUTOSIZE)
    
    print("====================================")
    print("📷 컬러 사진 촬영을 시작합니다.")
    print(" - 사진 찍기: 's' 키 또는 스페이스바")
    print(" - 종료하기: 'q' 키")
    print("====================================")

    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.01)

            color_img = node.get_color_frame()

            if color_img is not None:
                # 화면 표시용 복사본 (글씨 쓰기 용도)
                display_img = color_img.copy()
                
                cv2.putText(display_img, f"Saved: {img_count}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                cv2.imshow("Camera View", display_img)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('s') or key == 32:
                if color_img is not None:
                    # 파일 이름 생성 및 저장 (컬러만)
                    color_filename = os.path.join(save_dir_color, f"tile_{img_count:04d}.jpg")
                    cv2.imwrite(color_filename, color_img) 
                    
                    print(f"[{img_count}] 찰칵! 📸 -> {color_filename}")
                    img_count += 1
                else:
                    print("아직 카메라 초기화 중입니다. 잠시만요!")

            elif key == ord('q'):
                print("촬영을 종료합니다.")
                break

    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()