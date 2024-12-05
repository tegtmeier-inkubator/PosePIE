from script.base import ScriptBase


class Navigation(ScriptBase):
    def setup(self) -> None:
        self.max_num_players = 1

        self.keyboard = self.add_keyboard()

    def update(self) -> None:
        self.keyboard.arrow_up = self.pose.person[0].swipe_up
        self.keyboard.arrow_down = self.pose.person[0].swipe_down
        self.keyboard.arrow_left = self.pose.person[0].swipe_left
        self.keyboard.arrow_right = self.pose.person[0].swipe_right
