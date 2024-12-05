from input_emulation.gamepad import Gamepad
from script.plugin import PluginBase


class GamepadPlugin(PluginBase):
    def __init__(self, gamepad: Gamepad):
        self._gamepad = gamepad

    def create(self) -> None:
        pass

    def pre_update(self) -> None:
        pass

    def post_update(self) -> None:
        self._gamepad.update()

    def destroy(self) -> None:
        pass
