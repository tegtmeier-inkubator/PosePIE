# Copyright (c) 2024, 2025 Daniel Stolpmann <dstolpmann@tegtmeier-inkubator.de>
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

        self.mouse.button_left = pointing.selecting
