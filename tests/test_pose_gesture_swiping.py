import numpy as np

from pose.gesture.swiping import Swiping
from tests.utils.pose import Pose
from utils.side import Side


class TestLeftHand:
    def test_left_hand_up(self) -> None:
        pose = Pose()
        swiping = Swiping(Side.LEFT)
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
        swiping = Swiping(Side.LEFT)
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
        swiping = Swiping(Side.LEFT)
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
        swiping = Swiping(Side.LEFT)
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
        swiping = Swiping(Side.LEFT)
        swiping.set_shoulder_width(0.4)

        for _ in range(10):
            result = swiping.parse_keypoints(pose.keypoints)

        assert result.up is False
        assert result.down is False
        assert result.left is False
        assert result.right is False

    def test_left_not_detected_keypoint_threshold(self) -> None:
        pose = Pose()
        swiping = Swiping(Side.LEFT)
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
        swiping = Swiping(Side.RIGHT)
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
        swiping = Swiping(Side.RIGHT)
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
        swiping = Swiping(Side.RIGHT)
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
        swiping = Swiping(Side.RIGHT)
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
        swiping = Swiping(Side.RIGHT)
        swiping.set_shoulder_width(0.4)

        for _ in range(10):
            result = swiping.parse_keypoints(pose.keypoints)

        assert result.up is False
        assert result.down is False
        assert result.left is False
        assert result.right is False

    def test_right_not_detected_keypoint_threshold(self) -> None:
        pose = Pose()
        swiping = Swiping(Side.RIGHT)
        swiping.set_shoulder_width(0.4)

        for y in np.linspace(1.0, 0.0, 10):
            pose.right_wrist = np.array([0.1, y, 0.5])
            result = swiping.parse_keypoints(pose.keypoints)

        assert result.up is False
        assert result.down is False
        assert result.left is False
        assert result.right is False
