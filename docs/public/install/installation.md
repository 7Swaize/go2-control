# Setup of go2-control system environment

<img width="800" height="450" alt="layers" src="https://github.com/user-attachments/assets/ca55d189-61ad-4161-a492-cc874f74ff88" />

Note: The order of installation is important. It is not in the order of the layers themselves.

# Create project folder
Create a folder named `go2-workspace` in your home directory. We will install all applicable dependencies in here.

```bash
mkdir ~/go2-workspace
cd ~/go2-workspace
```

# Install platform manual dependencies

## Anaconda Workspace Setup

1. Download and Install [Anaconda](https://www.anaconda.com/download)
2. Create workspace with Python v3.10
3. Activate the workspace
   
```bash
conda create --name dogenv python=3.10
conda activate dogenv
```

## Install Build Dependencies

Before proceeding with installing other dependencies, ensure the following dependencies are installed:

- CMake (version 3.22 or higher)
- GCC (version 9.4.0)
- Make

You can install the required packages on Ubuntu 20.04 with:

```bash
sudo apt-get update
sudo snap install cmake --classic
sudo apt-get install -y g++ build-essential libyaml-cpp-dev libeigen3-dev libboost-all-dev libspdlog-dev libfmt-dev clang libclang-dev
hash -r
```

## Layer 3 and 4: Dependency Installation

Install all following dependencies with instructions listed below first. It recommended to install dependencies in the following order.

1. [Layer 3 - Unitree SDK](dependencies/unitree-sdk.md)
2. [Layer 3 - Librealsense SDK](dependencies/librealsense-sdk.md)
3. [Layer 3 - Iceoryx2](dependencies/iceoryx2.md)
4. [Layer 3 - ROS2 Workspace](dependencies/ros2-ws.md)  (BUG - ISSUES WITH UBUNTU VERSION)
   
6. [Layer 4 - Mujoco Simulator](dependencies/mujoco-sim.md)


## Layer 2: Clone the 'go2-control' Repository

In this step, we will clone and build the go2-control wrapper code.  This will use PIP to build/install the custom python wrapper library.

```bash
cd ~/go2-workspace
git clone https://github.com/7Swaize/go2-control.git

cd go2-control
pip install .
```
