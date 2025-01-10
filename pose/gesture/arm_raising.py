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

from pose.gesture.base import GestureBase
from pose.keypoints import Keypoints
from utils.side import Side


@dataclass
class ArmRaisingResult:
    detected: bool


class ArmRaising(GestureBase[ArmRaisingResult]):
    def __init__(self, min_keypoint_conf: float, side: Side):
        self._min_keypoint_conf = min_keypoint_conf
        self._side = side

    def parse_keypoints(self, keypoints: Keypoints) -> ArmRaisingResult:
        if self._side is Side.LEFT:
            eye = keypoints.left_eye
            wrist = keypoints.left_wrist
        else:
            eye = keypoints.right_eye
            wrist = keypoints.right_wrist

        detected = wrist.conf > self._min_keypoint_conf and eye.conf > self._min_keypoint_conf and wrist.y < eye.y

        return ArmRaisingResult(detected)
