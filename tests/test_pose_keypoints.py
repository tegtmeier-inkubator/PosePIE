import numpy as np
import pytest

from pose.keypoints import Keypoint, Keypoints


class TestKeypoint:
    def test_members(self) -> None:
        keypoint = Keypoint(np.array([1.0, 2.0]), np.array(0.5))

        assert keypoint.x == 1.0
        assert keypoint.y == 2.0
        np.testing.assert_equal(keypoint.xy, [1.0, 2.0])
        assert keypoint.conf == 0.5

    def test_invalid_xy_input_dimension(self) -> None:
        with pytest.raises(AssertionError):
            _ = Keypoint(np.array([1.0]), np.array(0.5))

        with pytest.raises(AssertionError):
            _ = Keypoint(np.array([1.0, 2.0, 3.0]), np.array(0.5))

        with pytest.raises(AssertionError):
            _ = Keypoint(np.array([[1.0], [2.0]]), np.array(0.5))

    def test_invalid_conf_input_dimension(self) -> None:
        with pytest.raises(AssertionError):
            _ = Keypoint(np.array([1.0, 2.0]), np.array([0.5]))

    def test_repr(self) -> None:
        keypoint = Keypoint(np.array([1.0, 2.0]), np.array(0.5))

        assert repr(keypoint) == "(x=1.0, y=2.0, conf=0.5)"


class TestKeypoints:
    def test_members(self) -> None:
        keypoints_tpose = np.array(
            [
                [0.5, 0.9],  # Nose
                [0.45, 0.92],  # Left eye
                [0.55, 0.92],  # Right eye
                [0.4, 0.9],  # Left ear
                [0.6, 0.9],  # Right ear
                [0.3, 0.7],  # Left shoulder
                [0.7, 0.7],  # Right shoulder
                [0.2, 0.7],  # Left elbow
                [0.8, 0.7],  # Right elbow
                [0.1, 0.7],  # Left wrist
                [0.9, 0.7],  # Right wrist
                [0.4, 0.5],  # Left hip
                [0.6, 0.5],  # Right hip
                [0.4, 0.3],  # Left knee
                [0.6, 0.3],  # Right knee
                [0.4, 0.1],  # Left ankle
                [0.6, 0.1],  # Right ankle
            ]
        )

        conf = np.linspace(0.8, 1.0, keypoints_tpose.shape[0])

        keypoints = Keypoints(keypoints_tpose, conf)

        np.testing.assert_equal(keypoints.xy, keypoints_tpose)
        np.testing.assert_equal(keypoints.conf, conf)

        np.testing.assert_equal(keypoints.nose.xy, keypoints_tpose[0])
        np.testing.assert_equal(keypoints.nose.conf, conf[0])
        np.testing.assert_equal(keypoints.left_eye.xy, keypoints_tpose[1])
        np.testing.assert_equal(keypoints.left_eye.conf, conf[1])
        np.testing.assert_equal(keypoints.right_eye.xy, keypoints_tpose[2])
        np.testing.assert_equal(keypoints.right_eye.conf, conf[2])
        np.testing.assert_equal(keypoints.left_ear.xy, keypoints_tpose[3])
        np.testing.assert_equal(keypoints.left_ear.conf, conf[3])
        np.testing.assert_equal(keypoints.right_ear.xy, keypoints_tpose[4])
        np.testing.assert_equal(keypoints.right_ear.conf, conf[4])
        np.testing.assert_equal(keypoints.left_shoulder.xy, keypoints_tpose[5])
        np.testing.assert_equal(keypoints.left_shoulder.conf, conf[5])
        np.testing.assert_equal(keypoints.right_shoulder.xy, keypoints_tpose[6])
        np.testing.assert_equal(keypoints.right_shoulder.conf, conf[6])
        np.testing.assert_equal(keypoints.left_elbow.xy, keypoints_tpose[7])
        np.testing.assert_equal(keypoints.left_elbow.conf, conf[7])
        np.testing.assert_equal(keypoints.right_elbow.xy, keypoints_tpose[8])
        np.testing.assert_equal(keypoints.right_elbow.conf, conf[8])
        np.testing.assert_equal(keypoints.left_wrist.xy, keypoints_tpose[9])
        np.testing.assert_equal(keypoints.left_wrist.conf, conf[9])
        np.testing.assert_equal(keypoints.right_wrist.xy, keypoints_tpose[10])
        np.testing.assert_equal(keypoints.right_wrist.conf, conf[10])
        np.testing.assert_equal(keypoints.left_hip.xy, keypoints_tpose[11])
        np.testing.assert_equal(keypoints.left_hip.conf, conf[11])
        np.testing.assert_equal(keypoints.right_hip.xy, keypoints_tpose[12])
        np.testing.assert_equal(keypoints.right_hip.conf, conf[12])
        np.testing.assert_equal(keypoints.left_knee.xy, keypoints_tpose[13])
        np.testing.assert_equal(keypoints.left_knee.conf, conf[13])
        np.testing.assert_equal(keypoints.right_knee.xy, keypoints_tpose[14])
        np.testing.assert_equal(keypoints.right_knee.conf, conf[14])
        np.testing.assert_equal(keypoints.left_ankle.xy, keypoints_tpose[15])
        np.testing.assert_equal(keypoints.left_ankle.conf, conf[15])
        np.testing.assert_equal(keypoints.right_ankle.xy, keypoints_tpose[16])
        np.testing.assert_equal(keypoints.right_ankle.conf, conf[16])

    def test_invalid_keypoints_input_dimension(self) -> None:
        with pytest.raises(AssertionError):
            _ = Keypoints(np.zeros((16, 2)), np.zeros((17,)))

        with pytest.raises(AssertionError):
            _ = Keypoints(np.zeros((18, 2)), np.zeros((17,)))

        with pytest.raises(AssertionError):
            _ = Keypoints(np.zeros((17, 1)), np.zeros((17,)))

        with pytest.raises(AssertionError):
            _ = Keypoints(np.zeros((17, 3)), np.zeros((17,)))

    def test_invalid_conf_input_dimension(self) -> None:
        with pytest.raises(AssertionError):
            _ = Keypoints(np.zeros((17, 2)), np.zeros((16,)))

        with pytest.raises(AssertionError):
            _ = Keypoints(np.zeros((17, 2)), np.zeros((18,)))
