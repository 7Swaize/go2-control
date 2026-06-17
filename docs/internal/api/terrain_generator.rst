==================
Terrain Generation
==================

.. py:module:: go2sim
   :synopsis: Terrain generation module for MuJoCo environments.

.. py:class:: GeometryType(str, Enum)

   Enumeration of supported geometric shapes for the terrain generator.

   .. py:attribute:: PLANE
      :value: "plane"
   
   .. py:attribute:: SPHERE
      :value: "sphere"
   
   .. py:attribute:: CAPSULE
      :value: "capsule"
   
   .. py:attribute:: ELLIPSOID
      :value: "ellipsoid"
   
   .. py:attribute:: CYLINDER
      :value: "cylinder"
   
   .. py:attribute:: BOX
      :value: "box"


.. py:class:: TerrainGenerator

   A utility class to dynamically generate and modify MuJoCo XML scene files for the robot simulation environment.

   .. py:attribute:: ROBOT
      :type: str
      :value: "go2"

      The identifier of the robot model.

   .. py:attribute:: BASE_DIR
      :type: pathlib.Path

      The root directory of the module.

   .. py:attribute:: GENERATED_SCENE_PATH
      :type: pathlib.Path

      The file path where the generated scene is saved.

   .. py:attribute:: BASE_SCENE_PATH
      :type: pathlib.Path

      The file path to the baseline XML scene.

   .. py:method:: __init__() -> None

      Initializes the TerrainGenerator, parsing the generated and base XML scenes and setting up the root XML element pointers.

   .. py:method:: add_geometry(position: List[float] = [1.0, 0.0, 0.0], euler: List[float] = [0.0, 0.0, 0.0], size: List[float] = [0.1, 0.1, 0.1], geo_type: GeometryType = GeometryType.BOX) -> None

      Adds a generic geometry object to the MuJoCo worldbody.

      :param position: The [x, y, z] coordinates of the geometry. Defaults to [1.0, 0.0, 0.0].
      :type position: List[float]
      :param euler: The Euler angles [roll, pitch, yaw] for rotation. Defaults to [0.0, 0.0, 0.0].
      :type euler: List[float]
      :param size: The full size [x, y, z] of the geometry (halved internally for MuJoCo). Defaults to [0.1, 0.1, 0.1].
      :type size: List[float]
      :param geo_type: The type of geometry to add. Defaults to GeometryType.BOX.
      :type geo_type: GeometryType

   .. py:method:: add_stairs(init_pos: List[float] = [1.0, 0.0, 0.0], yaw: float = 0.0, width: float = 0.2, height: float = 0.15, length: float = 1.5, stair_nums: int = 10) -> None

      Generates a sequence of ascending stair geometries.

      :param init_pos: The starting [x, y, z] position of the stair sequence. Defaults to [1.0, 0.0, 0.0].
      :type init_pos: List[float]
      :param yaw: The yaw angle rotation of the stair sequence in radians. Defaults to 0.0.
      :type yaw: float
      :param width: The tread depth (width along the walking path) of each stair. Defaults to 0.2.
      :type width: float
      :param height: The vertical riser height of each stair. Defaults to 0.15.
      :type height: float
      :param length: The span length of each stair perpendicular to the walking path. Defaults to 1.5.
      :type length: float
      :param stair_nums: The total number of stairs to generate. Defaults to 10.
      :type stair_nums: int

   .. py:method:: add_suspend_stairs(init_pos: List[float] = [1.0, 0.0, 0.0], yaw: float = 1.0, width: float = 0.2, height: float = 0.15, length: float = 1.5, gap: float = 0.1, stair_nums: int = 10) -> None

      Generates a sequence of suspended (floating) stair geometries with vertical gaps.

      :param init_pos: The starting [x, y, z] position of the stair sequence. Defaults to [1.0, 0.0, 0.0].
      :type init_pos: List[float]
      :param yaw: The yaw angle rotation of the stair sequence in radians. Defaults to 1.0.
      :type yaw: float
      :param width: The tread depth of each suspended stair. Defaults to 0.2.
      :type width: float
      :param height: The overall vertical displacement between stairs. Defaults to 0.15.
      :type height: float
      :param length: The span length of each stair. Defaults to 1.5.
      :type length: float
      :param gap: The vertical gap distance removing volume from the riser area. Defaults to 0.1.
      :type gap: float
      :param stair_nums: The total number of suspended stairs to generate. Defaults to 10.
      :type stair_nums: int

   .. py:method:: add_rough_ground(init_pos: List[float] = [1.0, 0.0, 0.0], euler: List[float] = [0.0, -0.0, 0.0], nums: List[int] = [10, 10], box_size: List[float] = [0.5, 0.5, 0.5], box_euler: List[float] = [0.0, 0.0, 0.0], separation: List[float] = [0.2, 0.2], box_size_rand: List[float] = [0.05, 0.05, 0.05], box_euler_rand: List[float] = [0.2, 0.2, 0.2], separation_rand: List[float] = [0.05, 0.05]) -> None

      Generates a randomized rough terrain grid composed of multiple box geometries.

      :param init_pos: The starting [x, y, z] baseline position. Defaults to [1.0, 0.0, 0.0].
      :type init_pos: List[float]
      :param euler: The base Euler angles [roll, pitch, yaw] for the entire grid. Defaults to [0.0, -0.0, 0.0].
      :type euler: List[float]
      :param nums: A list representing the [x_count, y_count] of boxes in the grid. Defaults to [10, 10].
      :type nums: List[int]
      :param box_size: The baseline [x, y, z] size for each terrain box. Defaults to [0.5, 0.5, 0.5].
      :type box_size: List[float]
      :param box_euler: The baseline Euler orientation for each terrain box. Defaults to [0.0, 0.0, 0.0].
      :type box_euler: List[float]
      :param separation: The baseline [x, y] spacing between box centers. Defaults to [0.2, 0.2].
      :type separation: List[float]
      :param box_size_rand: The randomization limits for the size of each box. Defaults to [0.05, 0.05, 0.05].
      :type box_size_rand: List[float]
      :param box_euler_rand: The randomization limits for the orientation of each box. Defaults to [0.2, 0.2, 0.2].
      :type box_euler_rand: List[float]
      :param separation_rand: The randomization limits for the spacing between boxes. Defaults to [0.05, 0.05].
      :type separation_rand: List[float]

   .. py:method:: add_aruco_marker(position: List[float] = [1.0, 0.0, 0.0], euler: List[float] = [0.0, 0.0, 0.0], size: List[float] = [0.1, 0.1, 0.1], marker_num: int = 0) -> None

      Adds a textured ArUco marker box to the scene.

      :param position: The [x, y, z] coordinates of the marker. Defaults to [1.0, 0.0, 0.0].
      :type position: List[float]
      :param euler: The Euler angles [roll, pitch, yaw] for rotation. Defaults to [0.0, 0.0, 0.0].
      :type euler: List[float]
      :param size: The full size [x, y, z] of the marker geometry. Defaults to [0.1, 0.1, 0.1].
      :type size: List[float]
      :param marker_num: The ArUco marker ID (must be between 0 and 20 inclusive). Defaults to 0.
      :type marker_num: int
      :raises ValueError: If `marker_num` falls outside the 0-20 range.

   .. py:method:: save() -> None

      Formats and saves the current state of the generated XML scene to the active path.

   .. py:method:: reset_to_base() -> None

      Overwrites the generated scene with the clean baseline scene and resets internal XML pointers.

   .. py:method:: load_scene_from_path(path: str) -> None

      Loads an external MuJoCo XML scene, sets it as the active generation target, and updates internal pointers.

      :param path: The absolute or relative file path to the target XML file.
      :type path: str
      :raises FileNotFoundError: If the provided path does not exist.

   .. py:method:: export_scene_to_directory(path: str) -> None

      Exports the current generated scene tree as 'scene.xml' to a specified directory.

      :param path: The path to the destination directory.
      :type path: str
      :raises FileNotFoundError: If the destination directory does not exist.