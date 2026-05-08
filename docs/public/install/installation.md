# Clone the Repository

```bash
git clone https://github.com/7Swaize/go2-control.git
```

# Dependency Installation

You should install all dependencies first. It recommended to install dependencies in the following order.

1. [Unitree SDK](dependencies/unitree-sdk.md)
2. [Librealsense SDK](dependencies/librealsense-sdk.md)
3. [Iceoryx2](dependencies/iceoryx2.md)
4. [Mujoco Simulator](dependencies/mujoco-sim.md)
5. [ROS2 Workspace](dependencies/ros2-ws.md)


# Main SDK Installation

Install via pip.

```bash
cd go2-control/go2
pip install .
```

(Optional) Create an editable install.

```bash
cd go2-control/go2
pip install -e .
```