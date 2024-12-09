import numpy as np
from script.base import ScriptBase


class Mouse(ScriptBase):
    def setup(self) -> None:
        self.max_num_players = 1

        self.mouse = self.add_mouse(absolute=True)

        self.shoulder_width = 0.0
        self.right_shoulder_xy = np.array([0.0, 0.0])

        self.xy = np.array([0.0, 0.0])

    def update(self) -> None:
        player = self.pose.person[0].keypoints

        if player.left_shoulder.conf > 0.8 and player.right_shoulder.conf > 0.8:
            alpha = 0.2
            self.right_shoulder_xy = alpha * player.right_shoulder.xy + (1 - alpha) * self.right_shoulder_xy
            self.shoulder_width = alpha * abs(player.left_shoulder.x - player.right_shoulder.x) + (1 - alpha) * self.shoulder_width

        if self.shoulder_width is not None and player.right_wrist.conf > 0.8 and player.right_shoulder.conf > 0.8:
            xy = (player.right_wrist.xy - self.right_shoulder_xy) / self.shoulder_width
            xy[1] *= 16 / 9

            if (np.abs(xy) < 1.25).all():
                xy = np.clip(xy / 2.0 + 0.5, 0.0, 1.0)

                alpha = 0.5
                self.xy = alpha * xy + (1 - alpha) * self.xy

                self.mouse.move_absolute.x = 1.0 - self.xy[0]
                self.mouse.move_absolute.y = self.xy[1]
