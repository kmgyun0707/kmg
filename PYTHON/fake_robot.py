import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Image
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped, Quaternion
from tf2_ros import TransformBroadcaster
import math
import numpy as np
import cv2  # OpenCV 추가
from cv_bridge import CvBridge # ROS 이미지 변환기 추가

class FakeTurtleBot(Node):
    def __init__(self):
        super().__init__('fake_turtlebot_publisher')

        # 1. 퍼블리셔 설정 (LiDAR, Odom, +Camera)
        self.scan_pub = self.create_publisher(LaserScan, 'scan', 10)
        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        # 카메라 토픽 추가 (RGB 640x480)
        self.image_pub = self.create_publisher(Image, '/camera/color/image_raw', 10)
        
        # 2. 유틸리티 설정
        self.tf_broadcaster = TransformBroadcaster(self)
        self.cv_bridge = CvBridge() # OpenCV 이미지를 ROS 메시지로 바꾸는 도구

        # 3. 타이머 설정 (0.1초 = 10Hz)
        self.timer = self.create_timer(0.1, self.timer_callback)

        # 상태 변수들
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.frame_count = 0 # 애니메이션용 카운터

    def get_quaternion_from_euler(self, roll, pitch, yaw):
        qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        return Quaternion(x=qx, y=qy, z=qz, w=qw)

    def timer_callback(self):
        current_time = self.get_clock().now()
        
        # --- [1. 가짜 이미지 생성 및 발행] ---
        # 빈 캔버스 생성 (높이 480, 너비 640, 3채널)
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # 움직이는 초록색 원 그리기 (웹사이트 딜레이 테스트용)
        # 프레임마다 x 좌표를 이동시킴
        circle_x = (self.frame_count * 10) % 640
        cv2.circle(img, (circle_x, 240), 50, (0, 255, 0), -1) # (B, G, R) 순서
        
        # 텍스트 정보 표시
        cv2.putText(img, f"Frame: {self.frame_count}", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(img, "Simulation Mode", (20, 100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # OpenCV -> ROS Image 메시지 변환
        ros_image_msg = self.cv_bridge.cv2_to_imgmsg(img, encoding="bgr8")
        ros_image_msg.header.stamp = current_time.to_msg()
        ros_image_msg.header.frame_id = "camera_link"
        
        self.image_pub.publish(ros_image_msg)
        self.frame_count += 1

        # --- [2. 기존 로봇 이동 로직 (Odom & TF)] ---
        dt = 0.1
        v, w = 0.2, 0.2
        self.theta += w * dt
        self.x += v * np.cos(self.theta) * dt
        self.y += v * np.sin(self.theta) * dt
        q = self.get_quaternion_from_euler(0, 0, self.theta)

        # Odom 발행
        odom_msg = Odometry()
        odom_msg.header.stamp = current_time.to_msg()
        odom_msg.header.frame_id = 'odom'
        odom_msg.child_frame_id = 'base_link'
        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.orientation = q
        self.odom_pub.publish(odom_msg)

        # TF 발행
        t = TransformStamped()
        t.header.stamp = current_time.to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.rotation = q
        self.tf_broadcaster.sendTransform(t)

        # --- [3. LiDAR 발행] ---
        scan_msg = LaserScan()
        scan_msg.header.stamp = current_time.to_msg()
        scan_msg.header.frame_id = 'base_link'
        scan_msg.angle_min, scan_msg.angle_max = 0.0, 2*np.pi
        scan_msg.angle_increment = (2*np.pi)/360
        scan_msg.range_min, scan_msg.range_max = 0.12, 10.0
        scan_msg.ranges = (2.0 + np.random.normal(0, 0.05, 360)).tolist()
        self.scan_pub.publish(scan_msg)

        if self.frame_count % 10 == 0:
            self.get_logger().info(f'Publishing Image & Odom... Frame: {self.frame_count}')

def main(args=None):
    rclpy.init(args=args)
    node = FakeTurtleBot()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()