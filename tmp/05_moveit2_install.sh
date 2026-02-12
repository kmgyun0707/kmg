#!/bin/bash
set -e

mkdir -p ~/ws_moveit/src
cd ~/ws_moveit/src

git clone https://github.com/moveit/moveit2_tutorials.git
vcs import < moveit2_tutorials/moveit2_tutorials.repos

sudo apt install ros-humble-octomap-msgs
sudo apt install ros-humble-object-recognition-msgs
sudo apt install ros-humble-controller-interface
sudo apt install ros-humble-generate-parameter-library
sudo apt install ros-humble-eigen-stl-containers
sudo apt install ros-humble-realtime-tools
sudo apt install ros-humble-geometric-shapes
sudo apt install ros-humble-osqp-vendor
sudo apt install ros-humble-ruckig
sudo apt install ros-humble-srdfdom
sudo apt install ros-humble-stomp
sudo apt install ros-humble-controller-manager-msgs
sudo apt install ros-humble-ros-testing
sudo apt install ros-humble-warehouse-ros
sudo apt install ros-humble-ompl
sudo apt install ros-humble-py-binding-tools

rosdep update
rosdep install -r --from-paths . --ignore-src --rosdistro humble -y


cd ../

MAKEFLAGS="j1" colcon build --executor sequential --parallel-workers 1


source /opt/ros/humble/setup.bash
sudo apt update # && sudo apt dist-upgrade


sudo apt install ros-humble-moveit

sudo apt install ros-humble-rmw-cyclonedds-cpp
echo 'export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp' >> ~/.bashrc
source ~/.bashrc

exit 0
