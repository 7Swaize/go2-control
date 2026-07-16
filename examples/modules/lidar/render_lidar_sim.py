import numpy as np

from go2.core import Go2Controller, ModuleType, HardwareType, ExecutionMode
from go2.modules.video import CameraSourceFactory


def create_controller() -> Go2Controller:
    controller = Go2Controller(hardware_type=HardwareType.VIRTUAL, execution_mode=ExecutionMode.ADVANCED)
    
    controller.add_module(ModuleType.LIDAR)
    controller.add_module(ModuleType.VIDEO, camera_source=CameraSourceFactory.create_virtual_camera())

    return controller



def main() -> None:
    controller = create_controller()


if __name__ == '__main__':
    main()