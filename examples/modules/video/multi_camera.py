import cv2
import numpy as np

from go2.core import Go2Controller, ModuleType, HardwareType
from go2.modules.video import CameraSourceFactory, FrameResult


def create_controller() -> Go2Controller:
    # Create a Go2 Controller instance to access all provided funtionalities.
    # Here, we choose HardwareType.NATIVE because we want movements commands to be executed on the actual robot.
    controller = Go2Controller(hardware_type=HardwareType.NATIVE)

    # The VIDEO module is not a default module on the controller. Therefore, we must add it explicitly.
    # The module contructor takes in a 'camera_source' target where we say when camera we want to read frames from.
    # We can pass in a camera group if we want to read frames from multiple cameras.
    controller.add_module(ModuleType.VIDEO, camera_source=CameraSourceFactory.create_camera_group({
        "internal": CameraSourceFactory.create_native_camera(), # Access the Go2 internal camera
        "depth": CameraSourceFactory.create_depth_camera() # Access the mounted depth camera
    }))

    return controller


def read_internal_camera(frame_result: FrameResult) -> None:
    if not frame_result.has_color():
        return

    # Do something with frame


def read_depth_camera(frame_result: FrameResult) -> None:
    # Depth cameras return both RGB and Depth frames. 
    
    # We can check if the frame container has both a color and depth frame available.
    if frame_result.is_fully_valid():
        color, depth = frame_result.color, frame_result.depth

        # Apply a heat colormap to the depth frame
        depth_colormap = cv2.applyColorMap(
            cv2.convertScaleAbs(depth, alpha=0.03),
            cv2.COLORMAP_JET
        )

        combined = np.hstack((
            color,
            cv2.resize(depth_colormap, (color.shape[1], color.shape[0]))
        ))

        cv2.imshow("RealSense Depth Camera", combined)


if __name__ == "__main__":
    # Create a controller instance
    controller = create_controller()

    while True:
        # Since, we are reading from multiple camera targets, we get a 'MultiFrameResult' instead.
        multi_res = controller.video.get_frames()

        # Access the 'FrameResult' from the internal camera capture
        internal_res = multi_res["internal"] # Key defined from when we added the camera source initially

        # Access the 'FrameResult' from the depth camera capture
        depth_res = multi_res["depth"] # Key defined from when we added the camera source initially

        # Do something with each of the frames
        read_internal_camera(internal_res)
        read_depth_camera(depth_res)

        key = cv2.waitKey(10) & 0xFF
        if key == ord("q"):
            break

    # Safely shutdown the controller and release resources
    controller.safe_shutdown()

