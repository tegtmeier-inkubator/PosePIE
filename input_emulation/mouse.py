from dataclasses import dataclass
from sys import platform

import numpy as np

ABS_MAX = 65535


@dataclass
class _Movement:
    x: float = 0.0
    y: float = 0.0


if platform == "linux":
    import uinput

    class Mouse:
        def __init__(self, absolute: bool = False) -> None:
            self._absolute = absolute

            events = []

            if self._absolute:
                self.move_absolute = _Movement()
                events.extend(
                    [
                        uinput.ABS_X + (0, ABS_MAX, 0, 0),  # Min, max, fuzz, flat
                        uinput.ABS_Y + (0, ABS_MAX, 0, 0),
                    ]
                )
            else:
                self.move_relative = _Movement()
                events.extend([uinput.REL_X, uinput.REL_Y])

            self.button_left: bool = False
            self.button_right: bool = False
            events.extend([uinput.BTN_LEFT, uinput.BTN_RIGHT])

            self._device = uinput.Device(events)

        def update(self) -> None:
            if self._absolute:
                self._device.emit(uinput.ABS_X, int(np.clip(int(self.move_absolute.x * ABS_MAX), 0, ABS_MAX)), syn=False)
                self._device.emit(uinput.ABS_Y, int(np.clip(int(self.move_absolute.y * ABS_MAX), 0, ABS_MAX)), syn=False)
            else:
                self._device.emit(uinput.REL_X, int(self.move_relative.x), syn=False)
                self._device.emit(uinput.REL_Y, int(self.move_relative.y), syn=False)

            self._device.emit(uinput.BTN_LEFT, int(self.button_left), syn=False)
            self._device.emit(uinput.BTN_RIGHT, int(self.button_right), syn=False)

            self._device.syn()

else:

    class Mouse:  # type: ignore[no-redef]
        def __init__(self, absolute: bool = False) -> None:
            raise NotImplementedError(f"Mouse not supported on platform {platform}!")
