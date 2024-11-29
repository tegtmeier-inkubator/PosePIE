import uinput

from script.base import ScriptBase


class Navigation(ScriptBase):
    def setup(self) -> None:
        self.max_num_players = 1

        self.keyboard = uinput.Device([uinput.KEY_UP, uinput.KEY_DOWN, uinput.KEY_LEFT, uinput.KEY_RIGHT])

    def update(self) -> None:
        self.keyboard.emit(uinput.KEY_UP, int(self.pose.person[0].swipe_up))
        self.keyboard.emit(uinput.KEY_DOWN, int(self.pose.person[0].swipe_down))
        self.keyboard.emit(uinput.KEY_LEFT, int(self.pose.person[0].swipe_left))
        self.keyboard.emit(uinput.KEY_RIGHT, int(self.pose.person[0].swipe_right))
