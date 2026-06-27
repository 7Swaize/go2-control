import cv2
import threading
import numpy as np
import iceoryx2 as iox2
from typing import Optional
from typing_extensions import override
from iceoryx_interfaces.camera_data import FrameData_
from iceoryx_interfaces.qos import CameraQoS

from .camera_source import CameraSource
from ..frame_result import FrameResult


class VirtualCameraSource(CameraSource):
    def __init__(self) -> None:
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._latest_frames: Optional[tuple[np.ndarray, np.ndarray]] = None
        self._initialize_iox_services()

    @override
    def _start(self) -> None:
        self._thread = threading.Thread(target=self._iox_thread, daemon=True)
        self._thread.start()

    def _initialize_iox_services(self) -> None:
        iox2.set_log_level_from_env_or(iox2.LogLevel.Error)

        # Kill signal handling: https://github.com/eclipse-iceoryx/iceoryx2/issues/528
        self._node = iox2.NodeBuilder.new() \
                        .signal_handling_mode(iox2.SignalHandlingMode.Disabled) \
                        .create(iox2.ServiceType.Ipc)

        self._cam_service = self._node.service_builder(iox2.ServiceName.new(CameraQoS.TOPIC_SIM_CAMERA)) \
                                .publish_subscribe(FrameData_) \
                                .max_publishers(CameraQoS.MAX_PUBLISHERS) \
                                .max_subscribers(CameraQoS.MAX_SUBSCRIBERS) \
                                .subscriber_max_buffer_size(CameraQoS.SUBSCRIBER_MAX_BUFFER_SIZE) \
                                .subscriber_max_borrowed_samples(CameraQoS.SUBSCRIBER_MAX_BORROWED_SAMPLES) \
                                .history_size(CameraQoS.HISTORY_SIZE) \
                                .open_or_create()


        self._cam_sub = self._cam_service.subscriber_builder().create()
        self._cycle_time = iox2.Duration.from_millis(1)


    def _iox_thread(self) -> None:
        while not self._stop_event.is_set():
            self._node.wait(self._cycle_time)

            sample = self._cam_sub.receive()
            if sample is None:
                continue

            msg = sample.payload().contents
            h, w = msg.height, msg.width

            rgb = cv2.cvtColor(
                np.array(msg.rgb_data, copy=True, dtype=np.uint8 ).reshape((h, w, 3))[::-1],
                cv2.COLOR_RGB2BGR,
            )
            depth = np.array(msg.depth_data, copy=True, dtype=np.uint16).reshape((h, w))[::-1]

            self._latest_frames = (rgb, depth)  # atomic under GIL

    @override
    def _get_frames(self) -> FrameResult:
        pair = self._latest_frames
        if pair is None:
            return FrameResult.pending()

        self._latest_frames = None
        return FrameResult.color_and_depth(color=pair[0], depth=pair[1])

    @override
    def _shutdown(self) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join()
            self._thread = None