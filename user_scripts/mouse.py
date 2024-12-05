from script.base import ScriptBase


class Mouse(ScriptBase):
    def setup(self) -> None:
        self.max_num_players = 1

        self.mouse = self.add_mouse()

    def update(self) -> None:
        right_wrist = self.pose.person[0].keypoints.right_wrist

        if right_wrist.conf > 0.8:
            self.mouse.move_relative.x = (0.5 - right_wrist.x) * 100
            self.mouse.move_relative.y = -(0.5 - right_wrist.y) * 100
        else:
            self.mouse.move_relative.x = 0
            self.mouse.move_relative.y = 0
