FROM ros:jazzy

RUN apt-get update && apt-get install -y \
    python3-colcon-common-extensions \
    python3-rosdep \
    git \
    nano \
    vim \
    usbutils \
    v4l-utils \
    ros-jazzy-xacro \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-robot-state-publisher \
    ros-jazzy-rviz2 \
    ros-jazzy-teleop-twist-keyboard \
    && rm -rf /var/lib/apt/lists/* \
    source /opt/ros/jazzy/setup.bash
WORKDIR /workspace

CMD ["bash"]
