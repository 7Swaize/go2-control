# Librealsense SDK - RSUSB Build - Jetson Orin Nano
 
The Jetson Orin Nano is unique, so the source files must be manually built. This process takes approximately 30 minutes. CUDA GPU acceleration is optional — the RSUSB build is simpler and safer.

Installation directions adapted from: [Librealsense Documentation](https://github.com/realsenseai/librealsense/blob/master/doc/installation_jetson.md)

## Setup

Install Python dependencies.

```bash
conda install conda-forge::python-devtools
```

Note the path to your Python interpreter — you will need it during the build:

```bash
which python
```
 
## CUDA Configuration (Optional)
 
Check if the CUDA compiler is available:
 
```bash
nvcc --version
```
 
If the "Cuda compiler driver" is not shown, you can either build without CUDA support or install the tools manually. 

### Installing the CUDA Toolkit

Install the NVIDIA JetPack toolkit:

```bash
sudo apt install nvidia-jetpack
```

Verify the CUDA installation directory:

```bash
ls /usr/local | grep cuda
```
 
The expected output should be something like `cuda-12.6`.
 
Add the CUDA compiler and runtime library paths to `~/.bashrc`:

```bash
# Find CUDA compiler and link CUDA libs at runtime
export PATH=/usr/local/cuda-12.6/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-12.6/lib64:$LD_LIBRARY_PATH
```
 
Test that `nvcc` is recognized and outputs the correct version information:
```bash
nvcc --version
```


## Build
 
Download the build script:

```bash
cd ~ && wget https://raw.githubusercontent.com/realsenseai/librealsense/refs/heads/master/scripts/libuvc_installation.sh -O libuvc_installation.sh
```
 
Edit the build script to configure the CMake invocation. Replace `<python_interpreter>` with the path from the `which python` output above.

**With CUDA** — also replace `<cuda_compiler>` with the path to your CUDA compiler (e.g. `/usr/local/cuda-12.6/bin/nvcc`):

```bash
cmake ../ -DFORCE_LIBUVC=true -DBUILD_PYTHON_BINDINGS:bool=true \
        -DPYTHON_EXECUTABLE=<python_interpreter> \
        -DCMAKE_BUILD_TYPE=release \
        -DBUILD_WITH_CUDA=true \
        -DCMAKE_CUDA_COMPILER=<cuda_compiler>
```

**Without CUDA**:

```bash
cmake ../ -DFORCE_LIBUVC=true -DBUILD_PYTHON_BINDINGS:bool=true \
        -DPYTHON_EXECUTABLE=<python_interpreter> \
        -DCMAKE_BUILD_TYPE=release \
        -DBUILD_WITH_CUDA=false
```
 
Unplug the camera, then run the build script:
```bash
bash libuvc_installation.sh
```
 
Once the build completes, reboot, plug in the camera, and run the following command to test the installation. The RealSense viewer window should open.

```bash
realsense-viewer
```

To enable Python support, install the Python bindings in your conda environment:
```bash
pip install pyrealsense2
```


# Librealsense SDK - Virtual Machine

Runtime access to a Realsense Depth Camera in a VM is not supported. As documented,

> Due to the USB 3.0 translation layer between native hardware and virtual machine,
> the librealsense team does not support installation in a VM. If you choose to try it, we
> recommend using VMware Workstation Player, and not Oracle VirtualBox for proper
> emulation of the USB3 controller.

Therefore, two options exist:
1. Install just the `pyrealsense2` (C++ to Python) bindings.
2. Proceed with installation on VMware Workstation Player.


## Install just Pyrealsense2 Bindings

This installs the Python bindings for the Intel RealSense SDK, allowing Python code to interface with the RealSense runtime libraries.
However, installing `pyrealsense2` alone does **NOT** guarantee that a D435i camera can be accessed. Camera detection and access depend on the underlying hardware drivers, USB configurations, and the Realsense runtime.

We only install the package, so that any code that imports `pyrealsense2` can do so without exception.

Run the following.

```bash
pip install pyrealsense2
```


## Proceed with Installation on VMware Workstation Player

This has not been tested. As a user, you are responsible for all installations and troubleshooting performed as part of this setup.

More detailed information can be found [here](https://gitlab.uwaterloo.ca/awerner/librealsense/-/blob/v2.16.1/doc/installation.md).
