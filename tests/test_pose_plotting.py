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

from pose.plotting import get_player_color


class TestPlayerColor:
    def test_player_color(self) -> None:
        np.testing.assert_equal(get_player_color(0), (200, 0, 0))
        np.testing.assert_equal(get_player_color(1), (0, 0, 200))
        np.testing.assert_equal(get_player_color(2), (0, 200, 200))
        np.testing.assert_equal(get_player_color(3), (0, 200, 0))
        np.testing.assert_equal(get_player_color(4), (200, 0, 0))
        np.testing.assert_equal(get_player_color(5), (0, 0, 200))
        np.testing.assert_equal(get_player_color(6), (0, 200, 200))
        np.testing.assert_equal(get_player_color(7), (0, 200, 0))
