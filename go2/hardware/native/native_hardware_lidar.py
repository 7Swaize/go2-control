import os
import sys
import shutil
import signal
import subprocess
from typing_extensions import override

from ..hardware_interface_lidar import HardwareInterfaceLIDAR


class NativeHardwareLIDAR(HardwareInterfaceLIDAR):
    def __init__(self) -> None:
        self._ros_proc = None
        
    @override
    def _initialize(self):
        self._launch_ros()

    def _launch_ros(self) -> None:
        kwargs = dict()
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            # To detach child process: https://stackoverflow.com/questions/45911705/why-use-os-setsid-in-python
            kwargs["start_new_session"] = True 

        self._ros_proc = subprocess.Popen(
            ["ros2", "launch", "bringup", "lidar_processor.launch.py"],
            **kwargs
        )

    @override
    def _shutdown(self):
        if self._ros_proc and self._ros_proc.poll() is None:
            try:
                if sys.platform == "win32":
                    self._ros_proc.send_signal(signal.CTRL_BREAK_EVENT)
                else:
                    os.killpg(os.getpgid(self._ros_proc.pid), signal.SIGINT)
                self._ros_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._ros_proc.terminate()
                self._ros_proc.wait(timeout=5)
        if shutil.which("ros2") is None:
            return