import ctypes
import threading
import numpy as np
import iceoryx2 as iox2
from typing import Optional

from iceoryx_interfaces.qos import LidarQoS
from iceoryx_interfaces.lidar_data import LidarHeader_

from .utils.singleton import Singleton
    

class LidarBridge(metaclass=Singleton):
    def __init__(self) -> None:
        iox2.set_log_level_from_env_or(iox2.LogLevel.Error)
        self._node = iox2.NodeBuilder.new() \
            .signal_handling_mode(iox2.SignalHandlingMode.Disabled) \
            .create(iox2.ServiceType.Ipc)

        self._decoded_service = self._node.service_builder(iox2.ServiceName.new(LidarQoS.TOPIC_LIDAR_DECODED)) \
            .request_response(ctypes.c_uint32, iox2.Slice[ctypes.c_double]) \
            .response_header(LidarHeader_) \
            .open_or_create()
        
        self._decoded_server = self._decoded_service.publisher_builder() \
            .initial_max_slice_len(LidarQoS.INITIAL_SLICE_LEN_HINT) \
            .allocation_strategy(iox2.AllocationStrategy.PowerOfTwo) \
            .create()
        
        self._cycle_time = iox2.Duration.from_millis(10)
        self._active_request: Optional[iox2.ActiveRequest] = None
        
        self._stop_event = threading.Event()
        self._worker_thread = threading.Thread(target=self._run, daemon=True)
        self._worker_thread.start()


    def _run(self) -> None:
        while not self._stop_event.is_set():
            self._node.wait(self._cycle_time)

            self._active_request = self._decoded_server.receive()
            if self._active_request is not None:
                break
            

    def send_decoded(self, stamp_ns: int, array: np.ndarray) -> None:
        if not self._active_request or not self._active_request.is_connected:
            return

        array = np.ascontiguousarray(array, dtype=np.float64)
        required_memory_size = array.size
        sample = self._decoded_server.loan_slice_uninit(required_memory_size)

        rows, cols = array.shape
        sample.user_header().contents.stamp_ns = stamp_ns
        sample.user_header().contents.rows = rows
        sample.user_header().contents.cols = cols

        # Theres safe interop between 'np.float64' and 'ctypes.c_double'
        ctypes.memmove(sample.payload().payload_ptr, array.ctypes.data, array.nbytes)

        sample = sample.assume_init()
        sample.send()        


    def shutdown(self) -> None:
        self._stop_event.set()
        self._active_request = None
