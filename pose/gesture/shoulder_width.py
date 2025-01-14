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

from dataclasses import dataclass

import numpy as np

from pose.gesture.base import GestureBase
from pose.keypoints import Keypoints
from utils.filter import Ewma

SHOULDER_WIDTH_EWMA_TIME_CONSTANT = 0.5


@dataclass
class ShoulderWidthResult:
    detected: bool
    width: float


class ShoulderWidth(GestureBase[ShoulderWidthResult]):
    """Calculates the shoulder width."""

    def __init__(self, min_keypoint_conf: float) -> None:
        self._min_keypoint_conf = min_keypoint_conf

        self._shoulder_width: float = 0.0
        self._shoulder_width_ewma = Ewma(SHOULDER_WIDTH_EWMA_TIME_CONSTANT)

    def parse_keypoints(self, keypoints: Keypoints) -> ShoulderWidthResult:
        if keypoints.left_shoulder.conf > self._min_keypoint_conf and keypoints.right_shoulder.conf > self._min_keypoint_conf:
            shoulder_width = float(np.linalg.norm(keypoints.left_shoulder.xy - keypoints.right_shoulder.xy))
            self._shoulder_width = self._shoulder_width_ewma(shoulder_width)

            detected = True
        else:
            detected = False

        return ShoulderWidthResult(detected, self._shoulder_width)
