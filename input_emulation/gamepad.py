from dataclasses import dataclass

from typing import Any

import vgamepad as vg


@dataclass
class _Stick:
    x: float = 0.0
    y: float = 0.0


class Gamepad:
    def __init__(self) -> None:
        self._vg = vg.VX360Gamepad()

        self.stick_left = _Stick()
        self.stick_right = _Stick()
        self.left_trigger: float = 0.0
        self.right_trigger: float = 0.0

        self.button_a: bool = False
        self.button_b: bool = False
        self.button_x: bool = False
        self.button_y: bool = False
        self.button_lb: bool = False
        self.button_rb: bool = False
        self.button_lt: bool = False
        self.button_rt: bool = False
        self.button_lsb: bool = False
        self.button_rsb: bool = False
        self.button_start: bool = False
        self.button_back: bool = False
        self.button_guide: bool = False
        self.dpad_up: bool = False
        self.dpad_down: bool = False
        self.dpad_left: bool = False
        self.dpad_right: bool = False

    def _set_button(self, button: Any, state: bool) -> None:
        if state:
            self._vg.press_button(button)
        else:
            self._vg.release_button(button)

    def update(self) -> None:
        self._vg.left_joystick_float(x_value_float=self.stick_left.x, y_value_float=self.stick_left.y)
        self._vg.right_joystick_float(x_value_float=self.stick_right.x, y_value_float=self.stick_right.y)
        self._vg.left_trigger_float(value_float=1.0 if self.button_lt else self.left_trigger)
        self._vg.right_trigger_float(value_float=1.0 if self.button_rt else self.right_trigger)

        self._set_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A, self.button_a)
        self._set_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B, self.button_b)
        self._set_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X, self.button_x)
        self._set_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y, self.button_y)
        self._set_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER, self.button_lb)
        self._set_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER, self.button_rb)
        self._set_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB, self.button_lsb)
        self._set_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB, self.button_rsb)
        self._set_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START, self.button_start)
        self._set_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK, self.button_back)
        self._set_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE, self.button_guide)
        self._set_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP, self.dpad_up)
        self._set_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN, self.dpad_down)
        self._set_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT, self.dpad_left)
        self._set_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT, self.dpad_right)

        self._vg.update()
