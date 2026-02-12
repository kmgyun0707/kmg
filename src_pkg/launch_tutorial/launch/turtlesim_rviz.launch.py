from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', PathJoinSubstitution([
                FindPackageShare('turtle_tf2_py'), 'rviz', 'turtle_rviz.rviz'])],
        ), #이건 rviz 실행 노드, 'turtle_tf2_py' 패키지의 rviz 디렉토리에 있는 turtle_rviz.rviz 설정 파일을 사용
    ])