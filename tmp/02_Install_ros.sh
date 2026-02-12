



# 필요한 모듈 설치

# git install
sudo apt update
sudo apt install git

sudo apt install python3-colcon-common-extensions python3-rosdep python3-ament-package python3-pyqt5 ros-humble-ament-cmake libzmq3-dev
export PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:$PKG_CONFIG_PATH

# 권한부여 
chmod +x ros2-humble-desktop-main.sh

# ros-2 설치 
./ros2-humble-desktop-main.sh


### Prerequisite installation elements before package installation
sudo apt update

sudo apt-get install -y libpoco-dev libyaml-cpp-dev
sudo apt-get install -y ros-humble-control-msgs ros-humble-realtime-tools ros-humble-xacro ros-humble-joint-state-publisher-gui ros-humble-ros2-control ros-humble-ros2-controllers ros-humble-gazebo-msgs ros-humble-moveit-msgs dbus-x11

### install gazebo sim
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
sudo apt-get update
sudo apt-get install -y libignition-gazebo6-dev
sudo apt-get install -y ros-humble-gazebo-ros-pkgs ros-humble-moveit-msgs ros-humble-ros-gz-sim

### We assume that you have installed the ros-humble-desktop package using the apt-get command.
### We recommand the /home/<user_home>/ros2_ws/src

sudo apt-get install -y libpoco-dev libyaml-cpp-dev wget \
                        ros-humble-control-msgs ros-humble-realtime-tools ros-humble-xacro \
                        ros-humble-joint-state-publisher-gui ros-humble-ros2-control \
                        ros-humble-ros2-controllers ros-humble-gazebo-msgs ros-humble-moveit-msgs \
                        dbus-x11 ros-humble-moveit-configs-utils ros-humble-moveit-ros-move-group \
                        ros-humble-gazebo-ros-pkgs ros-humble-ros-gz-sim ros-humble-ign-ros2-control

source ~/.bashrc
