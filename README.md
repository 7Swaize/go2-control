# Go2 Control

A Python SDK for controlling the Unitree Go2 robot and Mujoco Simulator via attachable modules.

For Ben Schepens.

## Installation - How To Setup The Simulator Environment

The wrapper targets **Ubuntu 22.04**. The MuJoCo simulator, however, is also compatible with **Ubuntu 24.04**. However, execution of this wrapper on the robot itself under **Ubuntu 24.04** is not guaranteed to work.

For installation instructions, see [here](docs/public/install/installation.md).


## Examples - How To Start Coding With The Simulator

Below are sample files demonstrating how to progammatically interact with the virtual go2 robot in the mujoco environment.  Start with these to write your own programs.

- [Movement Examples](examples/modules/movement/movement.md) — Examples for working with the controller's movement capabilities
- [Video Examples](examples/modules/video/video.md) — Examples for working with the controller's video capabilities
- [OCR Examples](examples/modules/ocr/ocr.md) — Examples for working with the controller's OCR capabilties
- [Terrain Generator Examples](examples/terrain_generator/terrain_generator.md) — Examples for working with the simulator's terrain generation capabilties
- [Aruko Marker Examples](examples/aruko_markers//aruko_markers.md) — Examples for detecting and reacting to Aruko markers


## Documentation

[API Documentation](https://go2-control.readthedocs.io/en/latest/)

[FAQ](docs/public/FAQ.md)

[Directory Structure](docs/public/repo_structure.md)


## GSMST Reference Information

Reference information regarding device and environment can be found [here](refs)
