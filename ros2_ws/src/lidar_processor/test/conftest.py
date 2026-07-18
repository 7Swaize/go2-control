import gc
import pytest
from typing import Optional

@pytest.fixture(autouse=True)
def _reset_lidar_bridge_singleton():
    # We have to reset the singleton instance before and after every test
    from lidar_processor.utils.singleton import Singleton
    from lidar_processor.lidar_bridge import LidarBridge

    yield
    
    bridge: Optional[LidarBridge] = Singleton._instances.pop(LidarBridge, None)
    if bridge:
        bridge.shutdown()
        gc.collect()