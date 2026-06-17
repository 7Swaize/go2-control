# Terrain Generator Examples

This folder contains examples for working with the Mujoco simulator's terrain generation capabilities.
In Mujoco, models are defined statically within an XML file and loaded during runtime: there is no GUI like in Unity.

Writing directly to XML files can be confusing. 
Therefore, the Terrain Generator module attempts to abstract that away. Users can add geometry to a scene via a Python API.


# What's Here

- [add_aruco_markers.py](add_aruco_markers.py) — Add Aruco markers to the scene.
    These can be picked up by the simulator camera and parsed by the user. 
- [add_geometry.py](add_geometry.py) — Add primitive objects to the scene.
