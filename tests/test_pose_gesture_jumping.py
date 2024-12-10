import numpy as np

from pose.gesture.jumping import Jumping
from tests.utils.pose import Pose


class TestJumping:
    def test_detected(self) -> None:
        pose = Pose()
        jumping = Jumping()
        jumping.set_shoulder_width(0.4)

        for y in np.linspace(0.7, 0.2, 10):
            pose.left_hip = np.array([0.6, y, 1.0])
            pose.right_hip = np.array([0.4, y, 1.0])
            result = jumping.parse_keypoints(pose.keypoints)

        assert result.detected is True

    def test_not_detected_no_movement(self) -> None:
        pose = Pose()
        jumping = Jumping()
        jumping.set_shoulder_width(0.4)

        for _ in range(10):
            result = jumping.parse_keypoints(pose.keypoints)

        assert result.detected is False

    def test_not_detected_down_movement(self) -> None:
        pose = Pose()
        jumping = Jumping()
        jumping.set_shoulder_width(0.4)

        for y in np.linspace(0.4, 0.6, 10):
            pose.left_hip = np.array([0.6, y, 1.0])
            pose.right_hip = np.array([0.4, y, 1.0])
            result = jumping.parse_keypoints(pose.keypoints)

        assert result.detected is False

    def test_not_detected_keypoint_threshold(self) -> None:
        pose = Pose()
        jumping = Jumping()
        jumping.set_shoulder_width(0.4)

        for y in np.linspace(0.6, 0.4, 10):
            pose.left_hip = np.array([0.6, y, 0.5])
            pose.right_hip = np.array([0.4, y, 0.5])
            result = jumping.parse_keypoints(pose.keypoints)

        assert result.detected is False
