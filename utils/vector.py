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

import numpy.typing as npt


class Vector2:
    def __init__(self, ndarray: npt.NDArray[np.float64]) -> None:
        assert ndarray.shape == (2,)

        self.xy = ndarray

    @property
    def x(self) -> float:
        return float(self.xy[0])

    @property
    def y(self) -> float:
        return float(self.xy[1])

    def __repr__(self) -> str:
        return f"(x={self.x}, y={self.y})"
