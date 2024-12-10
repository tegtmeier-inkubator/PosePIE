from script.base import ScriptBase


class Mouse(ScriptBase):
    def setup(self) -> None:
        self.max_num_players = 1

        self.mouse = self.add_mouse(absolute=True)

    def update(self) -> None:
        pointing = self.pose.person[0].right_hand_pointing

        if pointing.detected:
            xy = pointing.xy / 2 + 0.5

            self.mouse.move_absolute.x = 1.0 - xy[0]
            self.mouse.move_absolute.y = xy[1]
