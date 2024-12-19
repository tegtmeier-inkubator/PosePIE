# Copyright (c) 2024 Daniel Stolpmann <dstolpmann@tegtmeier-inkubator.de>
#
# This file is part of PosePIE.
#
# PosePIE is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# PosePIE is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with PosePIE. If
# not, see <https://www.gnu.org/licenses/>.

import numpy as np

from script.base import ScriptBase


class Trackmania(ScriptBase):
    def setup(self) -> None:
        self.max_num_players = 1

        self.gamepad = [self.add_gamepad() for _ in range(self.max_num_players)]

    def update(self) -> None:
        for player_id in range(self.max_num_players):
            self.gamepad[player_id].stick_left.x = np.clip(self.pose.person[player_id].steering.angle / 90, -1, 1)
            self.gamepad[player_id].stick_left.y = 0.0

            self.gamepad[player_id].button_a = self.pose.person[player_id].steering.detected
            self.gamepad[player_id].button_rb = self.pose.person[player_id].right_arm_raising.detected
