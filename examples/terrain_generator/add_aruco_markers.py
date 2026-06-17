import numpy as np
from go2sim import TerrainGenerator


# Adds six ArUco markers around the robot, oriented toward it and arranged in a circular pattern.
def add_aruco_markers(generator: TerrainGenerator) -> None:
    num_markers = 6
    radius = 3.0  # Distance from origin
    height = 0.4  # Lift slightly above ground
    size = [0.2, 0.2, 0.02]

    for i in range(num_markers):
        angle = 2 * np.pi * i / num_markers

        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        z = height

        # Direction from marker -> origin
        yaw = np.degrees(np.arctan2(-y, -x))
        euler = [0.0, 90.0, yaw]

        generator.add_aruco_marker(
            position=[x, y, z],
            euler=euler,
            size=size,
            marker_num=i
        )



generator = TerrainGenerator()

# Reset the scene to an empty scene.
generator.reset_to_base()

add_aruco_markers(generator)

# Write all added geometry to the internal xml file used my Mujoco
# Essentially, this saves all your changes.
# Without calling this method, any geometry added above will not be there when launching the simulator.
generator.save()