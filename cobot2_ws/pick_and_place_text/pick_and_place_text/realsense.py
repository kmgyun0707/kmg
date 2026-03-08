# 카메라 데이터를 수신하여 OpenCV 창에 표시하는 ROS2 노드입니다.
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge


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
    
    # 코드 추가
import rclpy
import cv2

# (여기에 원래 있던 ImgNode 클래스 코드가 들어갑니다)

def main(args=None):
    rclpy.init(args=args)
    node = ImgNode()

    # OpenCV 창 이름 설정
    cv2.namedWindow("Color Image", cv2.WINDOW_AUTOSIZE)
    
    print("카메라 데이터 수신을 시작합니다. (종료하려면 화면 클릭 후 'q' 누르기)")

    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.1)

            color_img = node.get_color_frame()
            depth_img = node.get_depth_frame()

            if color_img is not None and depth_img is not None:
                height, width = depth_img.shape
                center_x = int(width / 2)
                center_y = int(height / 2)

                distance_mm = depth_img[center_y, center_x]

                cv2.circle(color_img, (center_x, center_y), 5, (0, 0, 255), -1)
                cv2.putText(color_img, f"{distance_mm} mm", (center_x + 10, center_y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                cv2.imshow("Color Image", color_img)
            
            # 💡 수정된 부분: if문 바깥으로 빼서 데이터가 없어도 창이 안 뻗게 만듭니다.
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
 

    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
