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

from script.base import ScriptBase


class Navigation(ScriptBase):
    def setup(self) -> None:
        self.max_num_players = 1

        self.keyboard = self.add_keyboard()

    def update(self) -> None:
        self.keyboard.arrow_up = self.pose.person[0].right_hand_swiping.up
        self.keyboard.arrow_down = self.pose.person[0].right_hand_swiping.down
        self.keyboard.arrow_left = self.pose.person[0].right_hand_swiping.left
        self.keyboard.arrow_right = self.pose.person[0].right_hand_swiping.right
