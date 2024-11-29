import numpy as np

from script.base import ScriptBase


class Trackmania(ScriptBase):
    def setup(self) -> None:
        self.max_num_players = 1

    def update(self) -> None:
        for player_id in range(self.max_num_players):
            self.gamepad[player_id].stick_left.x = np.clip(self.pose.person[player_id].steering_angle / 90, -1, 1)
            self.gamepad[player_id].stick_left.y = 0.0

            self.gamepad[player_id].button_a = self.pose.person[player_id].accelerate
            self.gamepad[player_id].button_rb = self.pose.person[player_id].hand_center_diff[1] < -10
