import rclpy
from rclpy.node import Node
from rclpy.qos_overriding_options import QoSProfile
from ros_study_msgs.msg import MyMsg


class My_Msg_Test(Node):
    def __init__(self):
        super().__init__('my_msg_test_node')
        qos_profile = QoSProfile(depth=10)
        self.publisher_ = self.create_publisher(MyMsg, 'my_msg_topic', qos_profile)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0.0

    def timer_callback(self):
        msg = MyMsg()
        msg.num = self.i
        self.publisher_.publish(msg)
        self.get_logger().info(str(self.i)) #프린트문 같은거, 로그 남기는거
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    my_msg_test_publisher = My_Msg_Test()
    rclpy.spin(my_msg_test_publisher)
    my_msg_test_publisher.destroy_node()
    rclpy.shutdown()