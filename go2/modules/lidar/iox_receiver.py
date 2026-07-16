import ctypes
import threading
import numpy as np
import iceoryx2 as iox2
import numpy as np

from typing_extensions import override
from iceoryx_interfaces.qos import LidarQoS
from iceoryx_interfaces.lidar_data import LidarHeader_

from .callback_dispatcher import CallbackDispatcher


class IoxReceiver(threading.Thread):
    def __init__(self, dispatcher: CallbackDispatcher) -> None:
        super().__init__(daemon=True)
        self._dispatcher: CallbackDispatcher = dispatcher
        self._stop_event: threading.Event = threading.Event()
        self._init_iox2()

    def _init_iox2(self) -> None:
        iox2.set_log_level_from_env_or(iox2.LogLevel.Info)
        self._cycle_time = iox2.Duration.from_millis(50) # 20 Hz polling for ~11Hz Lidar: https://oss-global-cdn.unitree.com/static/52b72f707b304d229d4321eea223738f.pdf 
        self._node = iox2.NodeBuilder.new() \
                .signal_handling_mode(iox2.SignalHandlingMode.Disabled) \
                .create(iox2.ServiceType.Ipc)
        
        self._decoded_service = self._node.service_builder(iox2.ServiceName.new(LidarQoS.TOPIC_ROS_LIDAR_DECODED)) \
                                    .publish_subscribe(iox2.Slice[ctypes.c_double]) \
                                    .user_header(LidarHeader_) \
                                    .max_publishers(LidarQoS.MAX_PUBLISHERS) \
                                    .max_subscribers(LidarQoS.MAX_SUBSCRIBERS) \
                                    .subscriber_max_buffer_size(LidarQoS.SUBSCRIBER_MAX_BUFFER_SIZE) \
                                    .subscriber_max_borrowed_samples(LidarQoS.SUBSCRIBER_MAX_BORROWED_SAMPLES) \
                                    .history_size(LidarQoS.HISTORY_SIZE) \
                                    .open_or_create()

        self._decoded_sub = self._decoded_service.subscriber_builder().create()

    @override
    def run(self):
        while not self._stop_event.is_set():
            self._node.wait(self._cycle_time)

            while True:
                sample = self._decoded_sub.receive()
                if sample is None:
                    break
                
                data_ptr = ctypes.cast(sample.payload().as_ptr(), ctypes.POINTER(ctypes.c_double))

                self._dispatcher._emit_decoded(
                    sample.user_header().contents.stamp_ns,
                    np.ctypeslib.as_array(
                        data_ptr,
                        (sample.user_header().contents.rows, sample.user_header().contents.cols)
                    ).copy()
                )


    def _shutdown(self) -> None:
        self._stop_event.set()