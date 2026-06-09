# Mujoco Simulator Installation

This installation consists of two steps: first, installing the shared Iceoryx2 configuration files, and second, installing the actual simulator.


## Clone the Repository

```bash
cd ~/go2-workspace
git clone https://github.com/7Swaize/unitree_mujoco.git
cd unitree_mujoco
```


## Install Mujoco

The cloned repository depends on MuJoCo but does not include the library itself.  
You will need to install MuJoCo separately. Use release version **3.3.6**.

Navigate [here](https://github.com/google-deepmind/mujoco/releases/tag/3.3.6) and download the files for your system architecture.

Through the Linux GUI or command line:
1) Create the dirirctory ~/.mujoco
2) Change to ~/.mujoco
3) Extract the download mujoco file it to the `~/.mujoco` directory.
4) Remove the oringal zip file since it is no longer needed

```bash
cd ~/mujoco
cp ~/Downloads/mujo* .
tar -xvzf mujoco-3.3.6-linux-x86_64.tar.gz 

rm mujoco-3.3.6-linux-x86_64.tar.gz 
```

**Create a symlink to the Mujoco source.**

```bash
cd unitree_mujoco/simulate/
ln -s ~/.mujoco/mujoco-3.3.6 mujoco
```

## Shared Iceoryx2 Configuration Installation

This installation must be done before installing the actual simulator.

Set `CMAKE_PREFIX_PATH` to the installed **iceoryx2-cxx** location.

If you followed the default installation layout, the path will typically be: `<containing_folder>/iceoryx2/target/ff/cc/install`

To set the environment variable, run the following command in your terminal:

```bash
export CMAKE_PREFIX_PATH=<containing_folder>/iceoryx2/target/ff/cc/install
```

Install via CMake.

```bash
cd iceoryx_interfaces
cmake -S . -B build
cmake --build build
sudo cmake --install build
```

Install via pip.

```bash
pip install .
```


## Mujoco Simulator Installation

Install.

```bash
cd simulate
pip install .
```

(Optional) Install with verbose logging.

```bash
cd simulate
pip install . -v --config-settings=logging.level=INFO
```

Run the following command in the terminal to test the installation. It should launch the simulator.
```bash
go2sim
```
