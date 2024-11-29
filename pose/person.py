import math
import numpy as np

import numpy.typing as npt

from pose.keypoints import CocoPoseKeypoints
from utils.vector import Vector2


class Person:
    def __init__(self) -> None:
        self.keypoints = np.empty((17, 2))

        self.spine_angle = 0.0

        self._hand_center_diff = np.array([0.0, 0.0])
        self.steering_angle = 0.0
        self.accelerate = False

        self._hand_right_diff = np.array([0.0, 0.0])
        self.swipe_left = False
        self.swipe_right = False
        self.swipe_up = False
        self.swipe_down = False

        self._hand_right_old: npt.NDArray | None = None
        self._hand_center_old: npt.NDArray | None = None

    def _parse_spine_angle(self, keypoints: npt.NDArray, keypoints_scores: npt.NDArray) -> None:
        if (
            keypoints_scores[CocoPoseKeypoints.LEFT_SHOULDER] > 0.8
            and keypoints_scores[CocoPoseKeypoints.RIGHT_SHOULDER] > 0.8
            and keypoints_scores[CocoPoseKeypoints.LEFT_HIP] > 0.8
            and keypoints_scores[CocoPoseKeypoints.RIGHT_HIP] > 0.8
        ):
            shoulder_mid = (keypoints[CocoPoseKeypoints.LEFT_SHOULDER] + keypoints[CocoPoseKeypoints.RIGHT_SHOULDER]) / 2
            hip_mid = (keypoints[CocoPoseKeypoints.LEFT_HIP] + keypoints[CocoPoseKeypoints.RIGHT_HIP]) / 2
            spine_vector = hip_mid - shoulder_mid
            self.spine_angle = np.degrees(np.arctan2(spine_vector[0], spine_vector[1]))
        else:
            self.spine_angle = 0.0

    def _parse_steering(self, keypoints: npt.NDArray, keypoints_scores: npt.NDArray) -> None:
        if keypoints_scores[CocoPoseKeypoints.LEFT_WRIST] > 0.8 and keypoints_scores[CocoPoseKeypoints.RIGHT_WRIST] > 0.8:
            hand_center = (keypoints[CocoPoseKeypoints.LEFT_WRIST] + keypoints[CocoPoseKeypoints.RIGHT_WRIST]) / 2

            if self._hand_center_old is not None:
                alpha = 0.5
                self._hand_center_diff = (1 - alpha) * self._hand_center_diff + alpha * (hand_center - self._hand_center_old)
            self._hand_center_old = hand_center

            steering_vector = keypoints[CocoPoseKeypoints.LEFT_WRIST] - keypoints[CocoPoseKeypoints.RIGHT_WRIST]
            self.steering_angle = -math.degrees(math.atan2(steering_vector[1], steering_vector[0]))
            self.accelerate = True
        else:
            self._hand_center_old = None
            self._hand_center_diff = np.array([0.0, 0.0])

            self.steering_angle = 0.0
            self.accelerate = False

    @property
    def hand_center_diff(self) -> Vector2:
        return Vector2(self._hand_center_diff)

    def _parse_hand_swiping(self, keypoints: npt.NDArray, keypoints_scores: npt.NDArray) -> None:
        if keypoints_scores[CocoPoseKeypoints.RIGHT_WRIST] > 0.8:
            if self._hand_right_old is not None:
                alpha = 0.3
                self._hand_right_diff = (1 - alpha) * self._hand_right_diff + alpha * (
                    keypoints[CocoPoseKeypoints.RIGHT_WRIST] - self._hand_right_old
                )
            self._hand_right_old = keypoints[CocoPoseKeypoints.RIGHT_WRIST]
        else:
            self._hand_right_old = None
            self._hand_right_diff = np.array([0.0, 0.0])

        swipe_threshold_in = 8
        swipe_threshold_out = 1

        if self._hand_right_diff[0] > swipe_threshold_in:
            self.swipe_left = True
        elif self._hand_right_diff[0] < swipe_threshold_out / 2:
            self.swipe_left = False

        if self._hand_right_diff[0] < -swipe_threshold_in:
            self.swipe_right = True
        elif self._hand_right_diff[0] > -swipe_threshold_out / 2:
            self.swipe_right = False

        if self._hand_right_diff[1] < -swipe_threshold_in:
            self.swipe_up = True
        elif self._hand_right_diff[1] > -swipe_threshold_out / 2:
            self.swipe_up = False

        if self._hand_right_diff[1] > swipe_threshold_in:
            self.swipe_down = True
        elif self._hand_right_diff[1] < swipe_threshold_out / 2:
            self.swipe_down = False

    @property
    def hand_right_diff(self) -> Vector2:
        return Vector2(self._hand_right_diff)

    def parse_keypoints(self, keypoints: npt.NDArray, keypoints_scores: npt.NDArray) -> None:
        self.keypoints = keypoints

        self._parse_spine_angle(keypoints, keypoints_scores)
        self._parse_steering(keypoints, keypoints_scores)
        self._parse_hand_swiping(keypoints, keypoints_scores)
