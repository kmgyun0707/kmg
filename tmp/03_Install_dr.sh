mkdir -p ~/ros2_ws/src


cd ~/ros2_ws/src


git clone https://github.com/ROKEY-SPARK/DoosanBootcamp
git clone -b humble https://github.com/ros-controls/gz_ros2_control
rosdep install -r --from-paths . --ignore-src --rosdistro $ROS_DISTRO -y

cd DoosanBootcamp/

chmod +x ./install_emulator.sh
./install_emulator.sh
cd ~/ros2_ws
colcon build

# 만약 colcon build에서 warning(*error 발생은 안됨) 발생 시, 다시 colcon build

. install/setup.bash
export PYTHONPATH=$PYTHONPATH:~/ros2_ws/install/dsr_common2/lib/dsr_common2/imp
