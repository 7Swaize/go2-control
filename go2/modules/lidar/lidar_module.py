import numpy as np
from typing import Callable
from typing_extensions import override

from ...core.module import DogModule
from ...hardware.hardware_type import HardwareType
from ...hardware.hardware_interface_lidar import HardwareInterfaceLIDAR
from ...hardware.native.native_hardware_lidar import NativeHardwareLIDAR
from ...hardware.virtual.virtual_hardware_lidar import VirtualHardwareLIDAR
from .callback_dispatcher import CallbackDispatcher
from .iox_receiver import IoxReceiver


class LIDARModule(DogModule):
    """
    ``LIDARModule`` provides a simple API for:
        - Recieving decoded `PointCloud2` structures as xyz-intensity numpy arrays

    Users should interact **only** with this class and should not directly use other means of accessing lidar.
    
    Users should not access or construct this class directly.
    Rather, they should access it through the :class:`~core.controller.Go2Controller` instance.

    Important
    ---------
    - When executing on `HardwareType.Native' this module launches ROS2 nodes.
      In such a case, it is **critical** that students **ALWAYS** call :meth:`Go2Controller.safe_shutdown` after normal (error free) script exit.
    """

    def __init__(self) -> None:
        super().__init__("LIDAR")
        self._hardware: HardwareInterfaceLIDAR = None
        self._dispatcher: CallbackDispatcher = None
        self._iox_receiver: IoxReceiver = None

    @override
    def _initialize(self) -> None:
        """
        Initialize the lidar module. This is called internally,
        and should not be called directly by users.

        This method starts ROS2 process and Iceoryx2 pub-sub nodes for lidar data transfer.
        """
        if self._initialized:
            return

        if self._hardware_type == HardwareType.NATIVE:
            self._hardware = NativeHardwareLIDAR()
        else:
            self._hardware = VirtualHardwareLIDAR()

        self._hardware._initialize()
        self._launch_bridge()
        self._initialized = True

    # Rationale:
    # I dont want these handling deps to leak into the hardware abstraction.
    # Since they are shared across both abstractions, we can just keep it here.
    def _launch_bridge(self) -> None:
        self._dispatcher = CallbackDispatcher()
        self._iox_receiver = IoxReceiver(self._dispatcher)
        self._iox_receiver.start()

    def register_decoded_pointcloud_callback(self, callback: Callable[[int, np.ndarray], None]) -> None:
        """
        Register a callback to receive decoded PointCloud2 data.

        The callback is triggered whenever a new raw point cloud sample is received
        via Iceoryx2 and successfully reshaped.

        Parameters
        ----------
        callback : Callable[[int, np.ndarray], None]
            A function to be called with:
                - **timestamp** (int): The source timestamp in nanoseconds.
                - **points** (np.ndarray): A ``float64`` array of shape ``(N, 3)`` 
                  for [x, y, z] or ``(N, 4)`` if intensity is supported [x, y, z, intensity].

        Important
        ---------
        During each cycle, all subscribers receive **views** of the same underlying data.
        This is done for performance.
        Modifying data through the returned view is unsafe, as it affects the shared data.
        If you need to modify the data, create a **copy** first.
        """
        self._dispatcher._register_decoded(callback)


    @override
    def _shutdown(self) -> None:
        if self._hardware:
            self._hardware._shutdown()

        if self._iox_receiver:
            self._iox_receiver._shutdown()
            self._iox_receiver.join(timeout=2)

        self._initialized = False

