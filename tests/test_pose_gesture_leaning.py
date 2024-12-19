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
