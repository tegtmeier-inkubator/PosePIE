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

import numpy as np

from pose.gesture.pointing import Pointing, SELECTING_DELAY, SELECTING_REPETITION_INTERVAL
from tests.utils.pose import Pose
from utils.side import Side

MIN_KEYPOINT_CONF = 0.8


class TestLeftHand:
    def test_detected(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.LEFT)
        pointing.set_shoulder_width(0.4)

        result = pointing.parse_keypoints(pose.keypoints)

        assert result.detected is True

    def test_center(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.LEFT)
        pointing.set_shoulder_width(0.4)

        pose.left_wrist = pose.left_shoulder
        result = pointing.parse_keypoints(pose.keypoints)

        assert result.detected is True
        np.testing.assert_allclose(result.xy, [0.0, 0.0])

    def test_top_left(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.LEFT)
        pointing.set_shoulder_width(0.4)

        pose.left_wrist = pose.left_shoulder + np.array([-0.4, -0.4 / 16 * 9, 0.0])
        result = pointing.parse_keypoints(pose.keypoints)

        assert result.detected is True
        np.testing.assert_allclose(result.xy, [-1.0, -1.0])

    def test_bottom_right(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.LEFT)
        pointing.set_shoulder_width(0.4)

        pose.left_wrist = pose.left_shoulder + np.array([0.4, 0.4 / 16 * 9, 0.0])
        result = pointing.parse_keypoints(pose.keypoints)

        assert result.detected is True
        np.testing.assert_allclose(result.xy, [1.0, 1.0])

    def test_top_left_portrait(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.LEFT)
        pointing.set_aspect_ratio((9, 16))
        pointing.set_shoulder_width(0.4)

        pose.left_wrist = pose.left_shoulder + np.array([-0.4 / 16 * 9, -0.4, 0.0])
        result = pointing.parse_keypoints(pose.keypoints)

        assert result.detected is True
        np.testing.assert_allclose(result.xy, [-1.0, -1.0])

    def test_bottom_right_portrait(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.LEFT)
        pointing.set_aspect_ratio((9, 16))
        pointing.set_shoulder_width(0.4)

        pose.left_wrist = pose.left_shoulder + np.array([0.4 / 16 * 9, 0.4, 0.0])
        result = pointing.parse_keypoints(pose.keypoints)

        assert result.detected is True
        np.testing.assert_allclose(result.xy, [1.0, 1.0])

    def test_selecting(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.LEFT, timestamp=0.0)
        pointing.set_shoulder_width(0.4)

        result = pointing.parse_keypoints(pose.keypoints, timestamp=0.0)
        assert result.selecting is False

        # Initial
        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY - 0.01)
        assert result.selecting is False

        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY)
        assert result.selecting is True

        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY)
        assert result.selecting is False

        # 1. repetition
        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY + SELECTING_REPETITION_INTERVAL - 0.01)
        assert result.selecting is False

        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY + SELECTING_REPETITION_INTERVAL)
        assert result.selecting is True

        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY + SELECTING_REPETITION_INTERVAL)
        assert result.selecting is False

        # 2. repetition
        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY + 2 * SELECTING_REPETITION_INTERVAL - 0.01)
        assert result.selecting is False

        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY + 2 * SELECTING_REPETITION_INTERVAL)
        assert result.selecting is True

        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY + 2 * SELECTING_REPETITION_INTERVAL)
        assert result.selecting is False

        # Movement
        pose.left_wrist += np.array([0.2, 0.0, 0.0])

        # No 3. repetition
        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY + 3 * SELECTING_REPETITION_INTERVAL)
        assert result.detected is True
        assert result.selecting is False

    def test_not_detected_outside(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.LEFT)
        pointing.set_shoulder_width(0.4)

        pose.left_wrist = pose.left_shoulder + np.array([-0.5, -0.5 / 16 * 9, 0.0])
        result = pointing.parse_keypoints(pose.keypoints)

        assert result.detected is False

    def test_not_detected_keypoint_threshold(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.LEFT)
        pointing.set_shoulder_width(0.4)

        pose.left_wrist = np.array([pose.left_shoulder[0], pose.left_shoulder[1], 0.5])
        result = pointing.parse_keypoints(pose.keypoints)

        assert result.detected is False

    def test_not_detected_shoulder_width_zero(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.LEFT)
        pointing.set_shoulder_width(0.0)

        result = pointing.parse_keypoints(pose.keypoints)

        assert result.detected is False


class TestRightHand:
    def test_detected(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.RIGHT)
        pointing.set_shoulder_width(0.4)

        result = pointing.parse_keypoints(pose.keypoints)

        assert result.detected is True

    def test_center(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.RIGHT)
        pointing.set_shoulder_width(0.4)

        pose.right_wrist = pose.right_shoulder
        result = pointing.parse_keypoints(pose.keypoints)

        assert result.detected is True
        np.testing.assert_allclose(result.xy, [0.0, 0.0])

    def test_top_left(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.RIGHT)
        pointing.set_shoulder_width(0.4)

        pose.right_wrist = pose.right_shoulder + np.array([-0.4, -0.4 / 16 * 9, 0.0])
        result = pointing.parse_keypoints(pose.keypoints)

        assert result.detected is True
        np.testing.assert_allclose(result.xy, [-1.0, -1.0])

    def test_bottom_right(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.RIGHT)
        pointing.set_shoulder_width(0.4)

        pose.right_wrist = pose.right_shoulder + np.array([0.4, 0.4 / 16 * 9, 0.0])
        result = pointing.parse_keypoints(pose.keypoints)

        assert result.detected is True
        np.testing.assert_allclose(result.xy, [1.0, 1.0])

    def test_top_left_portrait(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.RIGHT)
        pointing.set_aspect_ratio((9, 16))
        pointing.set_shoulder_width(0.4)

        pose.right_wrist = pose.right_shoulder + np.array([-0.4 / 16 * 9, -0.4, 0.0])
        result = pointing.parse_keypoints(pose.keypoints)

        assert result.detected is True
        np.testing.assert_allclose(result.xy, [-1.0, -1.0])

    def test_bottom_right_portrait(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.RIGHT)
        pointing.set_aspect_ratio((9, 16))
        pointing.set_shoulder_width(0.4)

        pose.right_wrist = pose.right_shoulder + np.array([0.4 / 16 * 9, 0.4, 0.0])
        result = pointing.parse_keypoints(pose.keypoints)

        assert result.detected is True
        np.testing.assert_allclose(result.xy, [1.0, 1.0])

    def test_selecting(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.RIGHT, timestamp=0.0)
        pointing.set_shoulder_width(0.4)

        result = pointing.parse_keypoints(pose.keypoints, timestamp=0.0)
        assert result.selecting is False

        # Initial
        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY - 0.01)
        assert result.selecting is False

        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY)
        assert result.selecting is True

        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY)
        assert result.selecting is False

        # 1. repetition
        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY + SELECTING_REPETITION_INTERVAL - 0.01)
        assert result.selecting is False

        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY + SELECTING_REPETITION_INTERVAL)
        assert result.selecting is True

        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY + SELECTING_REPETITION_INTERVAL)
        assert result.selecting is False

        # 2. repetition
        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY + 2 * SELECTING_REPETITION_INTERVAL - 0.01)
        assert result.selecting is False

        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY + 2 * SELECTING_REPETITION_INTERVAL)
        assert result.selecting is True

        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY + 2 * SELECTING_REPETITION_INTERVAL)
        assert result.selecting is False

        # Movement
        pose.right_wrist += np.array([0.2, 0.0, 0.0])

        # No 3. repetition
        result = pointing.parse_keypoints(pose.keypoints, timestamp=SELECTING_DELAY + 3 * SELECTING_REPETITION_INTERVAL)
        assert result.detected is True
        assert result.selecting is False

    def test_not_detected_outside(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.RIGHT)
        pointing.set_shoulder_width(0.4)

        pose.right_wrist = pose.right_shoulder + np.array([-0.5, -0.5 / 16 * 9, 0.0])
        result = pointing.parse_keypoints(pose.keypoints)

        assert result.detected is False

    def test_not_detected_keypoint_threshold(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.RIGHT)
        pointing.set_shoulder_width(0.4)

        pose.right_wrist = np.array([pose.right_shoulder[0], pose.right_shoulder[1], 0.5])
        result = pointing.parse_keypoints(pose.keypoints)

        assert result.detected is False

    def test_not_detected_shoulder_width_zero(self) -> None:
        pose = Pose()
        pointing = Pointing(MIN_KEYPOINT_CONF, Side.RIGHT)
        pointing.set_shoulder_width(0.0)

        result = pointing.parse_keypoints(pose.keypoints)

        assert result.detected is False
