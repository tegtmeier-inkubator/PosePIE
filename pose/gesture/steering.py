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
from utils.vector import Vector2

DETECTION_FACTOR = 1.5


@dataclass
class SteeringResult:
    detected: bool
    angle: float


class Steering(GestureBase[SteeringResult]):
    def __init__(self, min_keypoint_conf: float) -> None:
        self._min_keypoint_conf = min_keypoint_conf

        self._shoulder_width: float = 0.0

    def set_shoulder_width(self, shoulder_width: float) -> None:
        self._shoulder_width = shoulder_width

    def parse_keypoints(self, keypoints: Keypoints) -> SteeringResult:
        if keypoints.left_wrist.conf > self._min_keypoint_conf and keypoints.right_wrist.conf > self._min_keypoint_conf:
            steering_vector = Vector2(keypoints.left_wrist.xy - keypoints.right_wrist.xy)

            detected = float(np.linalg.norm(steering_vector.xy)) < self._shoulder_width * DETECTION_FACTOR
            angle = float(-np.degrees(np.atan2(steering_vector.y, steering_vector.x)))
        else:
            detected = False
            angle = 0.0

        return SteeringResult(detected, angle)
