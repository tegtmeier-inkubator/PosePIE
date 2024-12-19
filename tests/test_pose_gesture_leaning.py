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

from pose.gesture.leaning import Leaning
from tests.utils.pose import Pose

MIN_KEYPOINT_CONF = 0.8


class TestLeaning:
    def test_zero_degrees(self) -> None:
        pose = Pose()
        leaning = Leaning(MIN_KEYPOINT_CONF)

        result = leaning.parse_keypoints(pose.keypoints)

        assert result.detected is True
        assert result.angle == 0.0

    def test_positive(self) -> None:
        pose = Pose()
        leaning = Leaning(MIN_KEYPOINT_CONF)

        pose.left_shoulder = np.array([0.6, 0.3, 1.0])
        pose.right_shoulder = np.array([0.2, 0.3, 1.0])
        pose.left_hip = np.array([0.6, 0.5, 1.0])
        pose.right_hip = np.array([0.4, 0.5, 1.0])
        result = leaning.parse_keypoints(pose.keypoints)

        assert result.detected is True
        assert result.angle > 0.0

    def test_negative(self) -> None:
        pose = Pose()
        leaning = Leaning(MIN_KEYPOINT_CONF)

        pose.left_shoulder = np.array([0.8, 0.3, 1.0])
        pose.right_shoulder = np.array([0.4, 0.3, 1.0])
        pose.left_hip = np.array([0.6, 0.5, 1.0])
        pose.right_hip = np.array([0.4, 0.5, 1.0])
        result = leaning.parse_keypoints(pose.keypoints)

        assert result.detected is True
        assert result.angle < 0.0

    def test_not_detected_keypoint_threshold(self) -> None:
        pose = Pose()
        leaning = Leaning(MIN_KEYPOINT_CONF)

        pose.left_shoulder = np.array([0.6, 0.3, 0.5])
        pose.right_shoulder = np.array([0.2, 0.3, 0.5])
        pose.left_hip = np.array([0.6, 0.5, 0.5])
        pose.right_hip = np.array([0.4, 0.5, 0.5])
        result = leaning.parse_keypoints(pose.keypoints)

        assert result.detected is False
        assert result.angle == 0.0
