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
from utils.vector import Vector2


@dataclass
class LeaningResult:
    detected: bool
    angle: float


class Leaning(GestureBase[LeaningResult]):
    """Calculates the angle of the spine to the vertical axis."""

    def __init__(self, min_keypoint_conf: float) -> None:
        self._min_keypoint_conf = min_keypoint_conf

    def parse_keypoints(self, keypoints: Keypoints) -> LeaningResult:
        if (
            keypoints.left_shoulder.conf > self._min_keypoint_conf
            and keypoints.right_shoulder.conf > self._min_keypoint_conf
            and keypoints.left_hip.conf > self._min_keypoint_conf
            and keypoints.right_hip.conf > self._min_keypoint_conf
        ):
            shoulder_mid_xy = (keypoints.left_shoulder.xy + keypoints.right_shoulder.xy) / 2
            hip_mid_xy = (keypoints.left_hip.xy + keypoints.right_hip.xy) / 2
            spine_vector = Vector2(hip_mid_xy - shoulder_mid_xy)

            detected = True
            angle = np.degrees(np.arctan2(spine_vector.x, spine_vector.y))
        else:
            detected = False
            angle = 0.0

        return LeaningResult(detected, angle)
