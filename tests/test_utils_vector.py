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
import pytest

from utils.vector import Vector2


class TestVector2:
    def test_members(self) -> None:
        vector = Vector2(np.array([1.0, 2.0]))

        assert vector.x == 1.0
        assert vector.y == 2.0
        np.testing.assert_equal(vector.xy, [1.0, 2.0])

    def test_invalid_input_dimension(self) -> None:
        with pytest.raises(AssertionError):
            _ = Vector2(np.array([1.0]))

        with pytest.raises(AssertionError):
            _ = Vector2(np.array([1.0, 2.0, 3.0]))

        with pytest.raises(AssertionError):
            _ = Vector2(np.array([[1.0], [2.0]]))

    def test_repr(self) -> None:
        vector = Vector2(np.array([1.0, 2.0]))

        assert repr(vector) == "(x=1.0, y=2.0)"
