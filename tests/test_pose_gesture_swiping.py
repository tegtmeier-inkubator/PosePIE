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

from pose.gesture.swiping import Swiping
from tests.utils.pose import Pose
from utils.side import Side

MIN_KEYPOINT_CONF = 0.8


class TestLeftHand:
    def test_left_hand_up(self) -> None:
        pose = Pose()
        swiping = Swiping(MIN_KEYPOINT_CONF, Side.LEFT)
        swiping.set_sensitivity(0.16)
        swiping.set_shoulder_width(0.4)

        for y in np.linspace(1.0, 0.0, 10):
            pose.left_wrist = np.array([0.9, y, 1.0])
            result = swiping.parse_keypoints(pose.keypoints)

        assert result.up is True
        assert result.down is False
        assert result.left is False
        assert result.right is False

    def test_left_hand_down(self) -> None:
        pose = Pose()
        swiping = Swiping(MIN_KEYPOINT_CONF, Side.LEFT)
        swiping.set_sensitivity(0.16)
        swiping.set_shoulder_width(0.4)

        for y in np.linspace(0.0, 1.0, 10):
            pose.left_wrist = np.array([0.9, y, 1.0])
            result = swiping.parse_keypoints(pose.keypoints)

        assert result.up is False
        assert result.down is True
        assert result.left is False
        assert result.right is False

    def test_left_hand_left(self) -> None:
        pose = Pose()
        swiping = Swiping(MIN_KEYPOINT_CONF, Side.LEFT)
        swiping.set_sensitivity(0.16)
        swiping.set_shoulder_width(0.4)

        for x in np.linspace(0.0, 1.0, 10):
            pose.left_wrist = np.array([x, 0.7, 1.0])
            result = swiping.parse_keypoints(pose.keypoints)

        assert result.up is False
        assert result.down is False
        assert result.left is True
        assert result.right is False

    def test_left_hand_right(self) -> None:
        pose = Pose()
        swiping = Swiping(MIN_KEYPOINT_CONF, Side.LEFT)
        swiping.set_sensitivity(0.16)
        swiping.set_shoulder_width(0.4)

        for x in np.linspace(1.0, 0.0, 10):
            pose.left_wrist = np.array([x, 0.7, 1.0])
            result = swiping.parse_keypoints(pose.keypoints)

        assert result.up is False
        assert result.down is False
        assert result.left is False
        assert result.right is True

    def test_left_not_detected_no_movement(self) -> None:
        pose = Pose()
        swiping = Swiping(MIN_KEYPOINT_CONF, Side.LEFT)
        swiping.set_sensitivity(0.16)
        swiping.set_shoulder_width(0.4)

        for _ in range(10):
            result = swiping.parse_keypoints(pose.keypoints)

        assert result.up is False
        assert result.down is False
        assert result.left is False
        assert result.right is False

    def test_left_not_detected_keypoint_threshold(self) -> None:
        pose = Pose()
        swiping = Swiping(MIN_KEYPOINT_CONF, Side.LEFT)
        swiping.set_sensitivity(0.16)
        swiping.set_shoulder_width(0.4)

        for y in np.linspace(1.0, 0.0, 10):
            pose.left_wrist = np.array([0.9, y, 0.5])
            result = swiping.parse_keypoints(pose.keypoints)

        assert result.up is False
        assert result.down is False
        assert result.left is False
        assert result.right is False


class TestRightHand:
    def test_right_hand_up(self) -> None:
        pose = Pose()
        swiping = Swiping(MIN_KEYPOINT_CONF, Side.RIGHT)
        swiping.set_sensitivity(0.16)
        swiping.set_shoulder_width(0.4)

        for y in np.linspace(1.0, 0.0, 10):
            pose.right_wrist = np.array([0.1, y, 1.0])
            result = swiping.parse_keypoints(pose.keypoints)

        assert result.up is True
        assert result.down is False
        assert result.left is False
        assert result.right is False

    def test_right_hand_down(self) -> None:
        pose = Pose()
        swiping = Swiping(MIN_KEYPOINT_CONF, Side.RIGHT)
        swiping.set_sensitivity(0.16)
        swiping.set_shoulder_width(0.4)

        for y in np.linspace(0.0, 1.0, 10):
            pose.right_wrist = np.array([0.1, y, 1.0])
            result = swiping.parse_keypoints(pose.keypoints)

        assert result.up is False
        assert result.down is True
        assert result.left is False
        assert result.right is False

    def test_right_hand_left(self) -> None:
        pose = Pose()
        swiping = Swiping(MIN_KEYPOINT_CONF, Side.RIGHT)
        swiping.set_sensitivity(0.16)
        swiping.set_shoulder_width(0.4)

        for x in np.linspace(0.0, 1.0, 10):
            pose.right_wrist = np.array([x, 0.7, 1.0])
            result = swiping.parse_keypoints(pose.keypoints)

        assert result.up is False
        assert result.down is False
        assert result.left is True
        assert result.right is False

    def test_right_hand_right(self) -> None:
        pose = Pose()
        swiping = Swiping(MIN_KEYPOINT_CONF, Side.RIGHT)
        swiping.set_sensitivity(0.16)
        swiping.set_shoulder_width(0.4)

        for x in np.linspace(1.0, 0.0, 10):
            pose.right_wrist = np.array([x, 0.7, 1.0])
            result = swiping.parse_keypoints(pose.keypoints)

        assert result.up is False
        assert result.down is False
        assert result.left is False
        assert result.right is True

    def test_right_not_detected_no_movement(self) -> None:
        pose = Pose()
        swiping = Swiping(MIN_KEYPOINT_CONF, Side.RIGHT)
        swiping.set_sensitivity(0.16)
        swiping.set_shoulder_width(0.4)

        for _ in range(10):
            result = swiping.parse_keypoints(pose.keypoints)

        assert result.up is False
        assert result.down is False
        assert result.left is False
        assert result.right is False

    def test_right_not_detected_keypoint_threshold(self) -> None:
        pose = Pose()
        swiping = Swiping(MIN_KEYPOINT_CONF, Side.RIGHT)
        swiping.set_sensitivity(0.16)
        swiping.set_shoulder_width(0.4)

        for y in np.linspace(1.0, 0.0, 10):
            pose.right_wrist = np.array([0.1, y, 0.5])
            result = swiping.parse_keypoints(pose.keypoints)

        assert result.up is False
        assert result.down is False
        assert result.left is False
        assert result.right is False
