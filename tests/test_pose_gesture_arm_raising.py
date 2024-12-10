import numpy as np

from pose.gesture.arm_raising import ArmRaising
from tests.utils.pose import Pose
from utils.side import Side


class TestLeftArm:
    def test_detected(self) -> None:
        pose = Pose()
        arm_raising = ArmRaising(Side.LEFT)

        pose.left_elbow = np.array([0.7, 0.05, 1.0])
        pose.left_wrist = np.array([0.7, 0.00, 1.0])
        result = arm_raising.parse_keypoints(pose.keypoints)

        assert result.detected is True

    def test_not_detected_pose(self) -> None:
        pose = Pose()
        arm_raising = ArmRaising(Side.LEFT)

        result = arm_raising.parse_keypoints(pose.keypoints)

        assert result.detected is False

    def test_not_detected_keypoint_threshold(self) -> None:
        pose = Pose()
        arm_raising = ArmRaising(Side.LEFT)

        pose.left_elbow = np.array([0.7, 0.05, 0.5])
        pose.left_wrist = np.array([0.7, 0.00, 0.5])
        result = arm_raising.parse_keypoints(pose.keypoints)

        assert result.detected is False


class TestRightArm:
    def test_detected(self) -> None:
        pose = Pose()
        arm_raising = ArmRaising(Side.RIGHT)

        pose.right_elbow = np.array([0.3, 0.05, 1.0])
        pose.right_wrist = np.array([0.3, 0.00, 1.0])
        result = arm_raising.parse_keypoints(pose.keypoints)

        assert result.detected is True

    def test_not_detected_pose(self) -> None:
        pose = Pose()
        arm_raising = ArmRaising(Side.RIGHT)

        result = arm_raising.parse_keypoints(pose.keypoints)

        assert result.detected is False

    def test_not_detected_keypoint_threshold(self) -> None:
        pose = Pose()
        arm_raising = ArmRaising(Side.RIGHT)

        pose.right_elbow = np.array([0.3, 0.05, 0.5])
        pose.right_wrist = np.array([0.3, 0.00, 0.5])
        result = arm_raising.parse_keypoints(pose.keypoints)

        assert result.detected is False
