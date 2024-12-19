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

from pose.gesture.steering import Steering
from tests.utils.pose import Pose

MIN_KEYPOINT_CONF = 0.8


class TestSteering:
    def test_zero_degrees(self) -> None:
        pose = Pose()
        steering = Steering(MIN_KEYPOINT_CONF)
        steering.set_shoulder_width(0.4)

        pose.left_wrist = np.array([0.6, 0.5, 1.0])
        pose.right_wrist = np.array([0.4, 0.5, 1.0])
        result = steering.parse_keypoints(pose.keypoints)

        assert result.detected is True
        assert result.angle == 0.0

    def test_plus_45_degrees(self) -> None:
        pose = Pose()
        steering = Steering(MIN_KEYPOINT_CONF)
        steering.set_shoulder_width(0.4)

        pose.left_wrist = np.array([0.6, 0.4, 1.0])
        pose.right_wrist = np.array([0.4, 0.6, 1.0])
        result = steering.parse_keypoints(pose.keypoints)

        assert result.detected is True
        assert result.angle == 45.0

    def test_plus_90_degrees(self) -> None:
        pose = Pose()
        steering = Steering(MIN_KEYPOINT_CONF)
        steering.set_shoulder_width(0.4)

        pose.left_wrist = np.array([0.5, 0.4, 1.0])
        pose.right_wrist = np.array([0.5, 0.6, 1.0])
        result = steering.parse_keypoints(pose.keypoints)

        assert result.detected is True
        assert result.angle == 90.0

    def test_minus_45_degrees(self) -> None:
        pose = Pose()
        steering = Steering(MIN_KEYPOINT_CONF)
        steering.set_shoulder_width(0.4)

        pose.left_wrist = np.array([0.6, 0.6, 1.0])
        pose.right_wrist = np.array([0.4, 0.4, 1.0])
        result = steering.parse_keypoints(pose.keypoints)

        assert result.detected is True
        assert result.angle == -45.0

    def test_minus_90_degrees(self) -> None:
        pose = Pose()
        steering = Steering(MIN_KEYPOINT_CONF)
        steering.set_shoulder_width(0.4)

        pose.left_wrist = np.array([0.5, 0.6, 1.0])
        pose.right_wrist = np.array([0.5, 0.4, 1.0])
        result = steering.parse_keypoints(pose.keypoints)

        assert result.detected is True
        assert result.angle == -90.0

    def test_not_detected_keypoint_threshold(self) -> None:
        pose = Pose()
        steering = Steering(MIN_KEYPOINT_CONF)
        steering.set_shoulder_width(0.4)

        pose.left_wrist = np.array([0.6, 0.5, 0.5])
        pose.right_wrist = np.array([0.4, 0.5, 0.5])
        result = steering.parse_keypoints(pose.keypoints)

        assert result.detected is False
        assert result.angle == 0.0

    def test_not_detected_distance(self) -> None:
        pose = Pose()
        steering = Steering(MIN_KEYPOINT_CONF)
        steering.set_shoulder_width(0.4)

        pose.left_wrist = np.array([0.8, 0.5, 1.0])
        pose.right_wrist = np.array([0.2, 0.5, 1.0])
        result = steering.parse_keypoints(pose.keypoints)

        assert result.detected is False
        assert result.angle == 0.0
