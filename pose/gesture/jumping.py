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

from pose.gesture.base import GestureBase
from pose.keypoints import Keypoints
from utils.filter import Derivative, Ewma
from utils.vector import Vector2

HIP_CENTER_EWMA_TIME_CONSTANT = 0.1
DEFAULT_SENSITIVITY = 0.4


@dataclass
class JumpingResult:
    detected: bool


class Jumping(GestureBase[JumpingResult]):
    def __init__(self, min_keypoint_conf: float) -> None:
        self._min_keypoint_conf = min_keypoint_conf

        self._shoulder_width: float = 0.0
        self._hip_center_diff = Derivative()
        self._hip_center_ewma = Ewma(HIP_CENTER_EWMA_TIME_CONSTANT)

        self._sensitivity: float = DEFAULT_SENSITIVITY

    def set_sensitivity(self, sensitivity: float) -> None:
        self._sensitivity = sensitivity

    def set_shoulder_width(self, shoulder_width: float) -> None:
        self._shoulder_width = shoulder_width

    def parse_keypoints(self, keypoints: Keypoints) -> JumpingResult:
        if keypoints.left_hip.conf > self._min_keypoint_conf and keypoints.right_hip.conf > self._min_keypoint_conf:
            hip_center = (keypoints.left_hip.xy + keypoints.right_hip.xy) / 2
            hip_center_diff = self._hip_center_ewma(self._hip_center_diff(hip_center))
        else:
            self._hip_center_diff.reset()
            self._hip_center_ewma.reset()
            hip_center_diff = np.array([0.0, 0.0])

        detected = Vector2(hip_center_diff).y < -self._shoulder_width / self._sensitivity

        return JumpingResult(detected)
