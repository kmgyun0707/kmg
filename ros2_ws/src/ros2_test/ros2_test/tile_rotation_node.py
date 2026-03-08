# rgb 이미지 토픽을 구독하여 타일의 회전 각도를 실시간으로 감지하는 ROS 2 노드입니다.
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class TileRotationNode(Node):
    def __init__(self):
        super().__init__('tile_rotation_node')
        
        # 1. ROS 2 <-> OpenCV 이미지 변환기
        self.bridge = CvBridge()
        
        # 2. 리얼센스 컬러 이미지 토픽 구독 (이름은 실제 토픽명에 맞게 확인 필요)
        self.image_sub = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',  # 리얼센스 기본 컬러 토픽
            self.image_callback,
            10
        )
        self.get_logger().info("📐 실시간 타일 회전 감지 노드가 시작되었습니다!")

    def image_callback(self, msg):
        """이미지 토픽이 들어올 때마다 실행되는 함수"""
        try:
            # ROS 이미지를 OpenCV 이미지(BGR)로 변환
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f"이미지 변환 실패: {e}")
            return

        # ---------------------------------------------------------
        # 여기서부터는 유닛테스트에서 검증하신 완벽한 OpenCV 로직입니다!
        # ---------------------------------------------------------
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 30, 100)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            if area > 5000:
                peri = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.04 * peri, True) # 윤곽선 근사화 (사각형 감지에 중요)
                
                if len(approx) == 4:
                    rect = cv2.minAreaRect(contour)
                    center, size, raw_angle = rect 

                    display_angle = raw_angle
                    
                    if display_angle > 45.0:
                        display_angle -= 90.0

                    # 터미널 창에도 로그를 찍어줍니다 (로봇 제어 디버깅용)
                    self.get_logger().info(f"타일 감지! 중심: {int(center[0])},{int(center[1])} | 각도: {display_angle:.1f}도")

                    # 화면 시각화 로직
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(frame, [box], 0, (0, 255, 0), 3) 
                    
                    text = f"Angle: {display_angle:.1f}"
                    cv2.putText(frame, text, (int(center[0])-50, int(center[1])), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # OpenCV 화면 출력 (콜백 함수 안에서는 waitKey(1)이 꼭 필요합니다!)
        cv2.imshow("Tile Rotation (ROS 2 Node)", frame)
        cv2.imshow("Debug Edges (ROS 2 Node)", closed)
        cv2.waitKey(1) 

def main(args=None):
    rclpy.init(args=args)
    node = TileRotationNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("노드를 종료합니다.")
    finally:
        node.destroy_node()
        cv2.destroyAllWindows()  # 노드 종료 시 화면 깔끔하게 닫기
        rclpy.shutdown()

if __name__ == '__main__':
    main()