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
from utils.filter import Derivative, Ewma
from utils.side import Side
from utils.vector import Vector2

POSITION_EWMA_TIME_CONSTANT = 0.1
DEFAULT_SENSITIVITY = 0.16
SWIPE_THRESHOLD_OUT_FACTOR = 0.25


@dataclass
class SwipingResult:
    left: bool
    right: bool
    up: bool
    down: bool


class Swiping(GestureBase[SwipingResult]):
    """Detects a swiping gesture."""

    def __init__(self, min_keypoint_conf: float, side: Side):
        self._min_keypoint_conf = min_keypoint_conf
        self._side = side

        self._shoulder_width: float = 0.0
        self._position_diff = Derivative()
        self._position_ewma = Ewma(POSITION_EWMA_TIME_CONSTANT)
        self._left: bool = False
        self._right: bool = False
        self._up: bool = False
        self._down: bool = False

        self._sensitivity = DEFAULT_SENSITIVITY

    def set_sensitivity(self, sensitivity: float) -> None:
        self._sensitivity = sensitivity

    def set_shoulder_width(self, shoulder_width: float) -> None:
        self._shoulder_width = shoulder_width

    def parse_keypoints(self, keypoints: Keypoints) -> SwipingResult:
        if self._side is Side.LEFT:
            wrist = keypoints.left_wrist
        else:
            wrist = keypoints.right_wrist

        if wrist.conf > self._min_keypoint_conf:
            position_diff = self._position_ewma(self._position_diff(wrist.xy))
        else:
            self._position_diff.reset()
            self._position_ewma.reset()
            position_diff = np.array([0.0, 0.0])

        swipe_threshold_in = self._shoulder_width / self._sensitivity
        swipe_threshold_out = swipe_threshold_in * SWIPE_THRESHOLD_OUT_FACTOR

        position_diff_vector = Vector2(position_diff)
        norm = np.linalg.norm(position_diff_vector.xy)
        angle = np.degrees(np.arctan2(-position_diff_vector.y, -position_diff_vector.x))

        if norm > swipe_threshold_in:
            self._left = bool(angle < -135 or angle > 135)
            self._right = bool(-45 < angle < 45)
            self._up = bool(45 < angle < 135)
            self._down = bool(-135 < angle < -45)
        elif norm < swipe_threshold_out:
            self._left = False
            self._right = False
            self._up = False
            self._down = False

        return SwipingResult(self._left, self._right, self._up, self._down)
