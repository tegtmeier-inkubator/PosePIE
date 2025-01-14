# Copyright (c) 2024, 2025 Daniel Stolpmann <dstolpmann@tegtmeier-inkubator.de>
#
# This file is part of PosePIE.
#
# PosePIE is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# PosePIE is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with PosePIE. If
# not, see <https://www.gnu.org/licenses/>.

from dataclasses import dataclass
from sys import platform

import numpy as np


@dataclass
class _Movement:
    x: float = 0.0
    y: float = 0.0


if platform == "linux":
    import uinput

    ABS_MAX = 65535

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

elif platform == "win32":
    import copy

    import win32api
    import win32con

    ABS_MAX = 65535

    class Mouse:  # type: ignore[no-redef]
        def __init__(self, absolute: bool = False) -> None:
            self._absolute = absolute

            if self._absolute:
                self.move_absolute = _Movement()
                self._move_absolute_old = copy.copy(self.move_absolute)
            else:
                self.move_relative = _Movement()

            self.button_left: bool = False
            self._button_left_old = self.button_left
            self.button_right: bool = False
            self._button_right_old = self.button_right

        def update(self) -> None:
            flags: int = 0

            if self.button_left != self._button_left_old:
                flags |= win32con.MOUSEEVENTF_LEFTDOWN if self.button_left else win32con.MOUSEEVENTF_LEFTUP
                self._button_left_old = self.button_left
            if self.button_right != self._button_right_old:
                flags |= win32con.MOUSEEVENTF_RIGHTDOWN if self.button_left else win32con.MOUSEEVENTF_RIGHTUP
                self._button_right_old = self.button_right

            if self._absolute:
                if self.move_absolute != self._move_absolute_old:
                    win32api.mouse_event(
                        win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE | flags,
                        int(np.clip(int(self.move_absolute.x * ABS_MAX), 0, ABS_MAX)),
                        int(np.clip(int(self.move_absolute.y * ABS_MAX), 0, ABS_MAX)),
                    )

                self._move_absolute_old = copy.copy(self.move_absolute)
            else:
                win32api.mouse_event(
                    win32con.MOUSEEVENTF_MOVE | flags,
                    int(self.move_relative.x),
                    int(self.move_relative.y),
                )

else:

    class Mouse:  # type: ignore[no-redef]
        def __init__(self, absolute: bool = False) -> None:
            raise NotImplementedError(f"Mouse not supported on platform {platform}!")
