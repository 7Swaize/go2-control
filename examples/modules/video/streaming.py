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
    # Here, we create an native camera to read frames from the Unitree Go2's internal camera.
    controller.add_module(ModuleType.VIDEO, camera_source=CameraSourceFactory.create_native_camera())

    return controller


def start_streaming(controller: Go2Controller) -> None:
    # Start the streaming server - only accessible on LAN devices
    controller.video.start_stream_server()

    # Print a link to the view the camera stream
    print(f"WebRTC streaming at: http://{controller.video.get_stream_server_local_ip()}:{controller.video.get_stream_server_port()}")


if __name__ == "__main__":
    # Create a controller instance
    controller = create_controller()

    while True:
        # Get a 'FrameResult' object from the video module.
        frame_result = controller.video.get_frames()

        # If the container object doesn't have a frame, we continue.
        if not frame_result.has_color():
            continue

        # Access frame
        color = frame_result.color

        # Annotate frame with something
        cv2.putText(
            color, 
            "This is an Annotation", 
            (50, 50), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            1, 
            (0, 255, 0), 
            2
        )

        # Send the annotated frame to the streamer
        controller.video.send_frame(color)

        key = cv2.waitKey(10) & 0xFF
        if key == ord("q"):
            break

    # Safely shutdown controller and release resources
    controller.safe_shutdown()
