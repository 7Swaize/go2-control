from abc import ABC, abstractmethod

class HardwareInterfaceLIDAR(ABC):
    """
    Abstract interface for lidar-related robot hardware control.

    This interface defines intialization and handling of communication reqeuired by the system.

    Notes
    -----
    - This is an internal abstraction.
    - Users should not subclass this directly.
    """

    @abstractmethod
    def _initialize(self) -> None:
        """
        Initialize the lidar hardware interface. This is handled automatically and shouldn't be called by users.
        Hardware initialization is linked to the core controller's initialization. The hardware is guaranteed to be 
        initialized before any other system provided by this package.

        Establishes communication with the native or virtual backend.
        """
        pass

    @abstractmethod
    def _shutdown(self) -> None:
        """
        Cleanly shut down the lidar hardware interface. This should not be called by users.
        """
        pass