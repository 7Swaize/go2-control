from go2sim import TerrainGenerator, GeometryType


def add_geometry(generator: TerrainGenerator) -> None:
    # Add a cube to the scene
    generator.add_geometry(position=[0.0, 2, 0.25], euler=[0.0, 0, 0.0], size=[0.5, 0.5, 0.5], geo_type=GeometryType.BOX)

    # Add ascending stairs to the scene
    generator.add_stairs(init_pos=[2.0, 4.0, 0.0], yaw=0.0)

    # Add ascending stairs with gaps between each step
    generator.add_suspend_stairs(init_pos=[1.0, 6.0, 0.0], yaw=0.0)



generator = TerrainGenerator()

# Reset the scene to an empty scene.
generator.reset_to_base()

add_geometry(generator)

# Write all added geometry to the internal xml file used my Mujoco
# Essentially, this saves all your changes.
# Without calling this method, any geometry added above will not be there when launching the simulator.
generator.save()