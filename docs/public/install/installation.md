# Setup of go2-control system environment

<< layers image >>

Note: The order of installation is important. It is not in the order of the layers themselves.

# Create project folder
Create a folder named `go2-workspace` in your home directory. We will install all applicable dependencies in here.

```bash
mkdir go2-workspace
cd go2-workspace
```

# Install platform manual dependencies

## Layer 3 and 4: Dependency Installation

Install all following dependencies with instructions listed below first. It recommended to install dependencies in the following order.

1. [Layer 3 - Unitree SDK](dependencies/unitree-sdk.md)
2. [Layer 3 - Librealsense SDK](dependencies/librealsense-sdk.md)
3. [Layer 3 - Iceoryx2](dependencies/iceoryx2.md)
4. [Layer 3 - ROS2 Workspace](dependencies/ros2-ws.md)
   
5. [Layer 4 - Mujoco Simulator](dependencies/mujoco-sim.md)


## Layer 2: Clone the 'go2-control' Repository

In this step, we will clone and build the go2-control wrapper code.  This will use PIP to build/install the custom python wrapper library.

```bash
git clone https://github.com/7Swaize/go2-control.git

cd go2-control/go2
pip install .
```
