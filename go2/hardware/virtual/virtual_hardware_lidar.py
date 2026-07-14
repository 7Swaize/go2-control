from typing_extensions import override

from ..hardware_interface_lidar import HardwareInterfaceLIDAR


class VirtualHardwareLIDAR(HardwareInterfaceLIDAR):
    @override
    def _initialize(self):
        pass

    @override
    def _shutdown(self):
        pass