import numpy as np

from pose.gesture.steering import Steering
from tests.utils.pose import Pose


class TestSteering:
    def test_zero_degrees(self) -> None:
        pose = Pose()
        steering = Steering()
        steering.set_shoulder_width(0.4)

        pose.left_wrist = np.array([0.6, 0.5, 1.0])
        pose.right_wrist = np.array([0.4, 0.5, 1.0])
        result = steering.parse_keypoints(pose.keypoints)

        assert result.detected is True
        assert result.angle == 0.0

    def test_plus_45_degrees(self) -> None:
        pose = Pose()
        steering = Steering()
        steering.set_shoulder_width(0.4)

        pose.left_wrist = np.array([0.6, 0.4, 1.0])
        pose.right_wrist = np.array([0.4, 0.6, 1.0])
        result = steering.parse_keypoints(pose.keypoints)

        assert result.detected is True
        assert result.angle == 45.0

    def test_plus_90_degrees(self) -> None:
        pose = Pose()
        steering = Steering()
        steering.set_shoulder_width(0.4)

        pose.left_wrist = np.array([0.5, 0.4, 1.0])
        pose.right_wrist = np.array([0.5, 0.6, 1.0])
        result = steering.parse_keypoints(pose.keypoints)

        assert result.detected is True
        assert result.angle == 90.0

    def test_minus_45_degrees(self) -> None:
        pose = Pose()
        steering = Steering()
        steering.set_shoulder_width(0.4)

        pose.left_wrist = np.array([0.6, 0.6, 1.0])
        pose.right_wrist = np.array([0.4, 0.4, 1.0])
        result = steering.parse_keypoints(pose.keypoints)

        assert result.detected is True
        assert result.angle == -45.0

    def test_minus_90_degrees(self) -> None:
        pose = Pose()
        steering = Steering()
        steering.set_shoulder_width(0.4)

        pose.left_wrist = np.array([0.5, 0.6, 1.0])
        pose.right_wrist = np.array([0.5, 0.4, 1.0])
        result = steering.parse_keypoints(pose.keypoints)

        assert result.detected is True
        assert result.angle == -90.0

    def test_not_detected_keypoint_threshold(self) -> None:
        pose = Pose()
        steering = Steering()
        steering.set_shoulder_width(0.4)

        pose.left_wrist = np.array([0.6, 0.5, 0.5])
        pose.right_wrist = np.array([0.4, 0.5, 0.5])
        result = steering.parse_keypoints(pose.keypoints)

        assert result.detected is False
        assert result.angle == 0.0

    def test_not_detected_distance(self) -> None:
        pose = Pose()
        steering = Steering()
        steering.set_shoulder_width(0.4)

        pose.left_wrist = np.array([0.8, 0.5, 1.0])
        pose.right_wrist = np.array([0.2, 0.5, 1.0])
        result = steering.parse_keypoints(pose.keypoints)

        assert result.detected is False
        assert result.angle == 0.0
