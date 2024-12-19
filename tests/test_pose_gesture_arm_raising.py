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

from pose.gesture.arm_raising import ArmRaising
from tests.utils.pose import Pose
from utils.side import Side

MIN_KEYPOINT_CONF = 0.8


class TestLeftArm:
    def test_detected(self) -> None:
        pose = Pose()
        arm_raising = ArmRaising(MIN_KEYPOINT_CONF, Side.LEFT)

        pose.left_elbow = np.array([0.7, 0.05, 1.0])
        pose.left_wrist = np.array([0.7, 0.00, 1.0])
        result = arm_raising.parse_keypoints(pose.keypoints)

        assert result.detected is True

    def test_not_detected_pose(self) -> None:
        pose = Pose()
        arm_raising = ArmRaising(MIN_KEYPOINT_CONF, Side.LEFT)

        result = arm_raising.parse_keypoints(pose.keypoints)

        assert result.detected is False

    def test_not_detected_keypoint_threshold(self) -> None:
        pose = Pose()
        arm_raising = ArmRaising(MIN_KEYPOINT_CONF, Side.LEFT)

        pose.left_elbow = np.array([0.7, 0.05, 0.5])
        pose.left_wrist = np.array([0.7, 0.00, 0.5])
        result = arm_raising.parse_keypoints(pose.keypoints)

        assert result.detected is False


class TestRightArm:
    def test_detected(self) -> None:
        pose = Pose()
        arm_raising = ArmRaising(MIN_KEYPOINT_CONF, Side.RIGHT)

        pose.right_elbow = np.array([0.3, 0.05, 1.0])
        pose.right_wrist = np.array([0.3, 0.00, 1.0])
        result = arm_raising.parse_keypoints(pose.keypoints)

        assert result.detected is True

    def test_not_detected_pose(self) -> None:
        pose = Pose()
        arm_raising = ArmRaising(MIN_KEYPOINT_CONF, Side.RIGHT)

        result = arm_raising.parse_keypoints(pose.keypoints)

        assert result.detected is False

    def test_not_detected_keypoint_threshold(self) -> None:
        pose = Pose()
        arm_raising = ArmRaising(MIN_KEYPOINT_CONF, Side.RIGHT)

        pose.right_elbow = np.array([0.3, 0.05, 0.5])
        pose.right_wrist = np.array([0.3, 0.00, 0.5])
        result = arm_raising.parse_keypoints(pose.keypoints)

        assert result.detected is False
