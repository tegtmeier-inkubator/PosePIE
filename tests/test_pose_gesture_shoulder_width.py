import numpy as np

from pose.gesture.shoulder_width import ShoulderWidth
from tests.utils.pose import Pose


class TestShoulderWidth:
    def test_width(self) -> None:
        pose = Pose()
        shoulder_width = ShoulderWidth()

        result = shoulder_width.parse_keypoints(pose.keypoints)

        assert result.detected is True
        np.testing.assert_almost_equal(result.width, 0.4)

    def test_not_detected_keypoint_threshold(self) -> None:
        pose = Pose()
        shoulder_width = ShoulderWidth()

        pose.left_shoulder = np.array([0.7, 0.3, 0.5])
        pose.right_shoulder = np.array([0.3, 0.3, 0.5])
        result = shoulder_width.parse_keypoints(pose.keypoints)

        assert result.detected is False
        assert result.width == 0.0
