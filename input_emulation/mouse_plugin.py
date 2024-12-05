from input_emulation.mouse import Mouse
from script.plugin import PluginBase


class MousePlugin(PluginBase):
    def __init__(self, mouse: Mouse):
        self._mouse = mouse

    def create(self) -> None:
        pass

    def pre_update(self) -> None:
        pass

    def post_update(self) -> None:
        self._mouse.update()

    def destroy(self) -> None:
        pass
