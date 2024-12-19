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

from pose.gesture.jumping import Jumping
from tests.utils.pose import Pose

MIN_KEYPOINT_CONF = 0.8


class TestJumping:
    def test_detected(self) -> None:
        pose = Pose()
        jumping = Jumping(MIN_KEYPOINT_CONF)
        jumping.set_shoulder_width(0.4)

        for y in np.linspace(0.7, 0.2, 10):
            pose.left_hip = np.array([0.6, y, 1.0])
            pose.right_hip = np.array([0.4, y, 1.0])
            result = jumping.parse_keypoints(pose.keypoints)

        assert result.detected is True

    def test_sensitivity(self) -> None:
        pose = Pose()
        jumping = Jumping(MIN_KEYPOINT_CONF)
        jumping.set_sensitivity(0.4)
        jumping.set_shoulder_width(0.4)

        for y in np.linspace(0.7, 0.2, 10):
            pose.left_hip = np.array([0.6, y, 1.0])
            pose.right_hip = np.array([0.4, y, 1.0])
            result = jumping.parse_keypoints(pose.keypoints)

        assert result.detected is True

    def test_not_detected_no_movement(self) -> None:
        pose = Pose()
        jumping = Jumping(MIN_KEYPOINT_CONF)
        jumping.set_shoulder_width(0.4)

        for _ in range(10):
            result = jumping.parse_keypoints(pose.keypoints)

        assert result.detected is False

    def test_not_detected_down_movement(self) -> None:
        pose = Pose()
        jumping = Jumping(MIN_KEYPOINT_CONF)
        jumping.set_shoulder_width(0.4)

        for y in np.linspace(0.4, 0.6, 10):
            pose.left_hip = np.array([0.6, y, 1.0])
            pose.right_hip = np.array([0.4, y, 1.0])
            result = jumping.parse_keypoints(pose.keypoints)

        assert result.detected is False

    def test_not_detected_keypoint_threshold(self) -> None:
        pose = Pose()
        jumping = Jumping(MIN_KEYPOINT_CONF)
        jumping.set_shoulder_width(0.4)

        for y in np.linspace(0.6, 0.4, 10):
            pose.left_hip = np.array([0.6, y, 0.5])
            pose.right_hip = np.array([0.4, y, 0.5])
            result = jumping.parse_keypoints(pose.keypoints)

        assert result.detected is False
