import cv2
import time

from go2.core import Go2Controller, ModuleType, HardwareType
from go2.modules.video import CameraSourceFactory


def create_controller() -> Go2Controller:
    # Create a Go2 Controller instance to access all provided funtionalities.
    # Here, we choose HardwareType.NATIVE because we want movements commands to be executed on the actual robot.
    controller = Go2Controller(hardware_type=HardwareType.NATIVE)

    # The VIDEO module is not a default module on the controller. Therefore, we must add it explicitly.
    # The module contructor takes in a 'camera_source' target where we say when camera we want to read frames from.
    # Here, we create an native camera to read frames from the Unitree Go2's internal camera.
    controller.add_module(ModuleType.VIDEO, camera_source=CameraSourceFactory.create_native_camera())

    return controller


if __name__ == "__main__":
    # Create a controller instance.
    controller = create_controller()

    while True:
        # Get a 'FrameResult' object from the video module.
        # This is a queryable container for a captured frame.
        frame_result = controller.video.get_frames()

        # If the container object doesn't have a frame, we continue.
        # This happens when we ask for frames faster than the capture rate on the camera or if an internal capture exception occurred.
        if not frame_result.has_color():
            continue

        # Display the frame using OpenCV
        cv2.imshow("Internal Go2 Camera", frame_result.color)

        key = cv2.waitKey(10) & 0xFF
        if key == ord("q"):
            break

    # Safely shutdown the controller and release resources
    controller.safe_shutdown()