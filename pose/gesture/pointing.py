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

from dataclasses import dataclass

import numpy as np

import numpy.typing as npt

from pose.gesture.base import GestureBase
from pose.keypoints import Keypoints
from utils.filter import Ewma
from utils.side import Side

DEFAULT_ASPECT_RATIO = 16 / 9
REFERENCE_SHOULDER_XY_EWMA_TIME_CONSTANT = 0.2
XY_EWMA_TIME_CONSTANT = 0.1
DETECTION_AREA_FACTOR = 1.25


@dataclass
class PointingResult:
    detected: bool
    xy: npt.NDArray[np.float64]


class Pointing(GestureBase[PointingResult]):
    def __init__(self, min_keypoint_conf: float, side: Side):
        self._min_keypoint_conf = min_keypoint_conf
        self._side = side

        self._aspect_ratio = DEFAULT_ASPECT_RATIO
        self._shoulder_width: float = 0.0
        self._reference_shoulder_xy = np.array([0.0, 0.0])
        self._reference_shoulder_xy_ewma = Ewma(REFERENCE_SHOULDER_XY_EWMA_TIME_CONSTANT)
        self._xy = np.array([0.0, 0.0])
        self._xy_ewma = Ewma(XY_EWMA_TIME_CONSTANT)

    def set_aspect_ratio(self, aspect_radio: tuple[float, float]) -> None:
        self._aspect_ratio = aspect_radio[0] / aspect_radio[1]

    def set_shoulder_width(self, shoulder_width: float) -> None:
        self._shoulder_width = shoulder_width

    def parse_keypoints(self, keypoints: Keypoints) -> PointingResult:
        if self._side is Side.LEFT:
            reference_shoulder = keypoints.left_shoulder
            wrist = keypoints.left_wrist
        else:
            reference_shoulder = keypoints.right_shoulder
            wrist = keypoints.right_wrist

        if reference_shoulder.conf > self._min_keypoint_conf:
            self._reference_shoulder_xy = self._reference_shoulder_xy_ewma(reference_shoulder.xy)

        detected = False
        if reference_shoulder.conf > self._min_keypoint_conf and wrist.conf > self._min_keypoint_conf and self._shoulder_width > 0.0:
            xy = (wrist.xy - self._reference_shoulder_xy) / self._shoulder_width
            if self._aspect_ratio > 1.0:
                xy[1] *= self._aspect_ratio
            elif self._aspect_ratio < 1.0:
                xy[0] /= self._aspect_ratio

            if (np.abs(xy) < DETECTION_AREA_FACTOR).all():
                xy = np.clip(xy, -1.0, 1.0)
                self._xy = self._xy_ewma(xy)

                detected = True
            else:
                self._xy_ewma.reset()
        else:
            self._xy_ewma.reset()

        return PointingResult(detected, self._xy)
