# ROS2 Humble - Installation

Installation directions adapted from: [ROS2 Humble Documentation](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html).

These are just the commands to install ROS2 Humble. For more guided or in depth directions, see the official ROS2 Humble documentation linked above.


## Set Locale

Make sure you have a locale which supports UTF-8.

```bash
locale  # check for UTF-8

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale  # verify settings
```


## Setup Sources

Ensure that the Ubuntu Universe repository is enabled.

To verify, run the following command:

```bash
apt-cache policy | grep universe
```

Part of the output should look similar to:

```bash
 500 http://ports.ubuntu.com/ubuntu-ports jammy-security/universe arm64 Packages
     release v=22.04,o=Ubuntu,a=jammy-security,n=jammy,l=Ubuntu,c=universe,b=arm64

```
**In case of error**
If you don't see lines similar to above indicating success, install the repository to your system with the following steps:

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
```


## Install Actual ROS packages 
Install the ros2-apt-source package to your system (after Ubunutu Universe is enabled).

```bash
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
```


## Install ROS2 Packages

Ensure system is up to date.

```bash
sudo apt update
sudo apt upgrade
```

Install the Desktop release for ROS2.

```bash
sudo apt install ros-humble-desktop
``` 


### Environment Setup

Set up your environment by sourcing the following file. This allows you to use the `ros2` CLI command.

```bash
source /opt/ros/humble/setup.bash
```

This must be done in every shell instance. Manually doing this can become repetitive, so you can add the command to your `.bashrc` file to have it automatically executed whenever a new terminal session is opened.


### Install Build Dependencies

Ensure system is up to date.

```bash
sudo apt update
sudo apt upgrade
```

Install colcon. This is needed to run the `colcon` CLI command to actually build our ROS2 workspace.

```bash
# You can choose to install to a venv, but be careful with interpreter paths when working with ROS2 
sudo apt install python3-colcon-common-extensions python3-catkin-pkg python3-lark-parser python3-empy
```



# C-Extensions - Installation

Install this dependency for our ROS2 nodes. 

```bash
cd go2-control/c_extensions
pip install .
```



# ROS2 Workspace - Installation

Build our ROS2 workspace.

```bash
source /opt/ros/humble/setup.bash

cd go2-control/ros2_ws
colcon build

source install/setup.bash
```
