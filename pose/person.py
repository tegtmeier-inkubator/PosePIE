import math
import numpy as np

import numpy.typing as npt

from pose.keypoints import Keypoints
from utils.vector import Vector2


class Person:
    def __init__(self) -> None:
        self.keypoints = Keypoints()

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

    def _parse_spine_angle(self, keypoints: Keypoints) -> None:
        if (
            keypoints.left_shoulder.conf > 0.8
            and keypoints.right_shoulder.conf > 0.8
            and keypoints.left_hip.conf > 0.8
            and keypoints.right_hip.conf > 0.8
        ):
            shoulder_mid_xy = (keypoints.left_shoulder.xy + keypoints.right_shoulder.xy) / 2
            hip_mid_xy = (keypoints.left_hip.xy + keypoints.right_hip.xy) / 2
            spine_vector = Vector2(hip_mid_xy - shoulder_mid_xy)
            self.spine_angle = np.degrees(np.arctan2(spine_vector.x, spine_vector.y))
        else:
            self.spine_angle = 0.0

    def _parse_steering(self, keypoints: Keypoints) -> None:
        if keypoints.left_wrist.conf > 0.8 and keypoints.right_wrist.conf > 0.8:
            hand_center = (keypoints.left_wrist.xy + keypoints.right_wrist.xy) / 2

            if self._hand_center_old is not None:
                alpha = 0.5
                self._hand_center_diff = (1 - alpha) * self._hand_center_diff + alpha * (hand_center - self._hand_center_old)
            self._hand_center_old = hand_center

            steering_vector = Vector2(keypoints.left_wrist.xy - keypoints.right_wrist.xy)
            self.steering_angle = -math.degrees(math.atan2(steering_vector.y, steering_vector.x))
            self.accelerate = True
        else:
            self._hand_center_old = None
            self._hand_center_diff = np.array([0.0, 0.0])

            self.steering_angle = 0.0
            self.accelerate = False

    @property
    def hand_center_diff(self) -> Vector2:
        return Vector2(self._hand_center_diff)

    def _parse_hand_swiping(self, keypoints: Keypoints) -> None:
        if keypoints.right_wrist.conf > 0.8:
            if self._hand_right_old is not None:
                alpha = 0.3
                self._hand_right_diff = (1 - alpha) * self._hand_right_diff + alpha * (keypoints.right_wrist.xy - self._hand_right_old)
            self._hand_right_old = keypoints.right_wrist.xy
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
        self.keypoints = Keypoints(keypoints, keypoints_scores)

        self._parse_spine_angle(self.keypoints)
        self._parse_steering(self.keypoints)
        self._parse_hand_swiping(self.keypoints)
