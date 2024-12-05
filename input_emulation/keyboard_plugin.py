from input_emulation.keyboard import Keyboard
from script.plugin import PluginBase


class KeyboardPlugin(PluginBase):
    def __init__(self, keyboard: Keyboard):
        self._keyboard = keyboard

    def create(self) -> None:
        pass

    def pre_update(self) -> None:
        pass

    def post_update(self) -> None:
        self._keyboard.update()

    def destroy(self) -> None:
        pass
