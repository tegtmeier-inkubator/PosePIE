from dataclasses import dataclass
from sys import platform


@dataclass
class _Movement:
    x: float = 0.0
    y: float = 0.0


if platform == "linux":
    import uinput

    class Mouse:
        def __init__(self) -> None:
            self._device = uinput.Device([uinput.REL_X, uinput.REL_Y, uinput.BTN_LEFT, uinput.BTN_RIGHT])

            self.move_relative = _Movement()

            self.button_left: bool = False
            self.button_right: bool = False

        def update(self) -> None:
            self._device.emit(uinput.REL_X, int(self.move_relative.x), syn=False)
            self._device.emit(uinput.REL_Y, int(self.move_relative.y), syn=False)

            self._device.emit(uinput.BTN_LEFT, int(self.button_left), syn=False)
            self._device.emit(uinput.BTN_RIGHT, int(self.button_right), syn=False)

            self._device.syn()

else:
    raise NotImplementedError(f"Mouse not supported on platform {platform}!")
