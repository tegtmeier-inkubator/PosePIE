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


class Keypoint:
    def __init__(
        self,
        xy: npt.NDArray[np.float64],
        conf: npt.NDArray[np.float64],
    ) -> None:
        assert xy.shape == (2,)
        assert conf.shape == ()

        self.xy = xy
        self._conf = conf

    @property
    def x(self) -> float:
        return float(self.xy[0])

    @property
    def y(self) -> float:
        return float(self.xy[1])

    @property
    def conf(self) -> float:
        return float(self._conf)

    def __repr__(self) -> str:
        return f"(x={self.x}, y={self.y}, conf={self.conf})"


class Keypoints:
    def __init__(
        self,
        xy: npt.NDArray[np.float64] = np.empty((17, 2)),
        conf: npt.NDArray[np.float64] = np.empty((17,)),
    ) -> None:
        assert xy.shape == (17, 2)
        assert conf.shape == (17,)

        self.xy = xy
        self.conf = conf

    @property
    def nose(self) -> Keypoint:
        return Keypoint(self.xy[0], self.conf[0])

    @property
    def left_eye(self) -> Keypoint:
        return Keypoint(self.xy[1], self.conf[1])

    @property
    def right_eye(self) -> Keypoint:
        return Keypoint(self.xy[2], self.conf[2])

    @property
    def left_ear(self) -> Keypoint:
        return Keypoint(self.xy[3], self.conf[3])

    @property
    def right_ear(self) -> Keypoint:
        return Keypoint(self.xy[4], self.conf[4])

    @property
    def left_shoulder(self) -> Keypoint:
        return Keypoint(self.xy[5], self.conf[5])

    @property
    def right_shoulder(self) -> Keypoint:
        return Keypoint(self.xy[6], self.conf[6])

    @property
    def left_elbow(self) -> Keypoint:
        return Keypoint(self.xy[7], self.conf[7])

    @property
    def right_elbow(self) -> Keypoint:
        return Keypoint(self.xy[8], self.conf[8])

    @property
    def left_wrist(self) -> Keypoint:
        return Keypoint(self.xy[9], self.conf[9])

    @property
    def right_wrist(self) -> Keypoint:
        return Keypoint(self.xy[10], self.conf[10])

    @property
    def left_hip(self) -> Keypoint:
        return Keypoint(self.xy[11], self.conf[11])

    @property
    def right_hip(self) -> Keypoint:
        return Keypoint(self.xy[12], self.conf[12])

    @property
    def left_knee(self) -> Keypoint:
        return Keypoint(self.xy[13], self.conf[13])

    @property
    def right_knee(self) -> Keypoint:
        return Keypoint(self.xy[14], self.conf[14])

    @property
    def left_ankle(self) -> Keypoint:
        return Keypoint(self.xy[15], self.conf[15])

    @property
    def right_ankle(self) -> Keypoint:
        return Keypoint(self.xy[16], self.conf[16])
