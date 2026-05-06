"""
Defines DDS topic names used internally by the system
for inter-process communication. These topics are used by ROS2 bridges,
LIDAR processing, and state monitoring.

Users should **not** use these directly; they are for internal
infrastructure and low-level module integration only.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class DDSTopics:
    LOW_STATE = "rt/lf/lowstate"
