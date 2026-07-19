import time

from go2.core import Go2Controller, HardwareType


def create_controller() -> Go2Controller:
    # Create a Go2 Controller instance to access all provided funtionalities.
    # Here, we choose HardwareType.VIRTUAL because we want movements commands to be executed in the simulation.
    controller = Go2Controller(hardware_type=HardwareType.VIRTUAL)

    # NOTE: The movement module is a default module. It is already added onto the controller.
    # Therefore, we do not need to explictly add it.

    return controller


def run_movement_sequence(controller: Go2Controller) -> None:
    controller.movement.stand_up()

    for _ in range(3):
        controller.movement.move(1, 0)

    controller.movement.stop()

    for _ in range(3):
        controller.movement.rotate(2)

    controller.movement.stop()
    controller.movement.stand_down()


if __name__ == "__main__":
    # Create a controller instance
    controller = create_controller()

    # Run our test movement sequence
    run_movement_sequence(controller)

    # Shutdown the controller
    # It is critical to always shutdown the control on script exit
    controller.safe_shutdown()