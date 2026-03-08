import numpy as np
import cv2
import rclpy
from rclpy.node import Node
from typing import Any, Callable, Optional, Tuple

from ament_index_python.packages import get_package_share_directory
from od_msg.srv import SrvDepthPosition
from pick_and_place_text.realsense import ImgNode
# YOLO 라이브러리 직접 임포트!
from ultralytics import YOLO

PACKAGE_NAME = 'pick_and_place_text'
PACKAGE_PATH = get_package_share_directory(PACKAGE_NAME)

class ObjectDetectionNode(Node):
    def __init__(self, model_name = 'yolo'):
        super().__init__('object_detection_node')
        self.img_node = ImgNode()
        
        # 🌟 방금 학습한 OBB 모델(best.pt)의 '절대 경로'를 입력해 줍니다.
        # 코랩에서 다운로드한 파일이나, 로컬에서 학습한 파일의 경로로 꼭 맞춰주세요!
        self.model_path = '/home/rokey/cobot_ws/src/cobot2_ws/model/yolov8n-obb_v1.pt'  # 예시 경로입니다. 실제 경로로 수정하세요.
        self.model = YOLO(self.model_path)
        
        self.intrinsics = self._wait_for_valid_data(
            self.img_node.get_camera_intrinsic, "camera intrinsics"
        )
        self.create_service(
            SrvDepthPosition,
            'get_3d_position',
            self.handle_get_depth
        )
        self.get_logger().info("🔥 OBB Object Detection Node initialized.")

    def handle_get_depth(self, request, response):
        """클라이언트 요청을 처리해 3D 좌표를 반환합니다."""
        self.get_logger().info(f"Received request: {request}")
        
        # 3D 좌표(x, y, z)와 회전 각도(angle)를 받아옵니다.
        coords_and_angle = self._compute_position(request.target)
        
        # 만약 SrvDepthPosition 서비스 메시지가 [x, y, z] 3개만 받는 배열이라면 앞의 3개만 넘깁니다.
        # (서비스에 angle을 추가하셨다면 response.depth_position = coords_and_angle 로 쓰세요!)
        response.depth_position = [float(val) for val in coords_and_angle[:3]] 
        
        return response

    def _compute_position(self, target):
        """이미지를 처리해 OBB 객체의 카메라 좌표와 회전 각도를 계산합니다."""
        rclpy.spin_once(self.img_node)

        # 1. 카메라에서 컬러 이미지를 가져옵니다.
        color_frame = self._wait_for_valid_data(self.img_node.get_color_frame, "color frame")

        # 2. YOLO OBB 모델로 객체를 탐지합니다.
        results = self.model(color_frame, verbose=False)

        # 3. 탐지된 객체가 없거나 OBB 데이터가 없으면 예외 처리
        if not results or results[0].obb is None or len(results[0].obb) == 0:
            self.get_logger().warn("No tile detection found.")
            # 실패 시 기본값 반환 (x, y, z, angle)
            return 0.0, 0.0, 0.0, 0.0 

        # 4. 가장 신뢰도(Confidence)가 높은 첫 번째 객체의 데이터를 가져옵니다.
        best_obb = results[0].obb[0]
        
        # 🌟 OBB 핵심: xywhr 속성에서 [중심x, 중심y, 너비, 높이, 라디안 각도] 를 추출합니다.
        cx, cy, w, h, angle = best_obb.xywhr[0].cpu().numpy()
        confidence = best_obb.conf[0].cpu().numpy()
        
        # 픽셀 좌표는 정수형이므로 변환
        cx_int, cy_int = int(cx), int(cy)
        
        # 화면에 잘 잡혔는지 로그로 띄워줍니다. (angle은 라디안 값이므로 보기 쉽게 각도(degree)로도 출력)
        degree = np.degrees(angle)
        self.get_logger().info(f"🎯 Tile Found! conf={confidence:.2f}, cx={cx_int}, cy={cy_int}, angle={degree:.1f}도")

        # 5. 해당 중심점 픽셀의 깊이(Depth) 값을 읽어옵니다.
        cz = self._get_depth(cx_int, cy_int)
        
        if cz is None or cz <= 0:
            self.get_logger().warn("Depth value is invalid or out of range.")
            return 0.0, 0.0, 0.0, 0.0

        # 6. 픽셀 좌표를 3D 카메라 좌표계로 변환합니다.
        x_3d, y_3d, z_3d = self._pixel_to_camera_coords(cx_int, cy_int, cz)

        # 3D 좌표와 회전 각도(라디안)를 함께 반환합니다.
        return x_3d, y_3d, z_3d, angle

    def _get_depth(self, x, y):
        """픽셀 좌표의 depth 값을 안전하게 읽어옵니다."""
        frame = self._wait_for_valid_data(self.img_node.get_depth_frame, "depth frame")
        try:
            return frame[y, x]
        except IndexError:
            self.get_logger().warn(f"Coordinates ({x},{y}) out of range.")
            return None

    def _wait_for_valid_data(self, getter, description):
        """getter 함수가 유효한 데이터를 반환할 때까지 spin 하며 재시도합니다."""
        data = getter()
        while data is None or (isinstance(data, np.ndarray) and not data.any()):
            rclpy.spin_once(self.img_node)
            # 로그 도배 방지를 위해 잠시 대기할 수도 있습니다.
            data = getter()
        return data

    def _pixel_to_camera_coords(self, x, y, z):
        """픽셀 좌표와 intrinsics를 이용해 카메라 좌표계로 변환합니다."""
        fx = self.intrinsics['fx']
        fy = self.intrinsics['fy']
        ppx = self.intrinsics['ppx']
        ppy = self.intrinsics['ppy']
        
        # Depth 카메라 단위(보통 mm)를 고려해야 할 경우 여기서 m 단위로 변환(/1000.0)을 적용할 수 있습니다.
        camera_x = (x - ppx) * z / fx
        camera_y = (y - ppy) * z / fy
        camera_z = z
        
        return camera_x, camera_y, camera_z

def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetectionNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()