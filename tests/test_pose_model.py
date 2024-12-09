import numpy as np
from pose.model import correct_aspect_ratio


class TestCorrectAspectRatio:
    def test_landscape(self) -> None:
        bboxes, keypoints = correct_aspect_ratio(
            (1080, 1920),
            np.array([[0.0, 0.0, 1.0, 1.0]]),
            np.array([[[0.0, 0.0, 0.5], [1.0, 1.0, 0.5], [0.5, 0.5, 0.5]]]),
        )
        np.testing.assert_equal(bboxes, [[0.0, 0.21875, 1.0, 0.78125]])
        np.testing.assert_equal(keypoints, [[[0.0, 0.21875, 0.5], [1.0, 0.78125, 0.5], [0.5, 0.5, 0.5]]])

    def test_portrait(self) -> None:
        bboxes, keypoints = correct_aspect_ratio(
            (1920, 1080),
            np.array([[0.0, 0.0, 1.0, 1.0]]),
            np.array([[[0.0, 0.0, 0.5], [1.0, 1.0, 0.5], [0.5, 0.5, 0.5]]]),
        )
        np.testing.assert_equal(bboxes, [[0.21875, 0.0, 0.78125, 1.0]])
        np.testing.assert_equal(keypoints, [[[0.21875, 0.0, 0.5], [0.78125, 1.0, 0.5], [0.5, 0.5, 0.5]]])
