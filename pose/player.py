import math
import numpy as np

import numpy.typing as npt

from pose.keypoints import CocoPoseKeypoints


class Player:
    def __init__(self) -> None:
        self.reset()

        self._hand_right_old: npt.NDArray | None = None
        self._hand_center_old: npt.NDArray | None = None

    def reset(self) -> None:
        self.spine_angle = 0.0
        self.hand_center_diff = np.array([0.0, 0.0])
        self.steering_angle = 0.0
        self.hand_right_diff = np.array([0.0, 0.0])
        self.swipe_left = False
        self.swipe_right = False
        self.swipe_up = False
        self.swipe_down = False
        self.accelerate = False

    def parse_keypoints(self, keypoints: npt.NDArray, keypoints_scores: npt.NDArray) -> None:
        if (
            keypoints_scores[CocoPoseKeypoints.LEFT_SHOULDER.value] > 0.8
            and keypoints_scores[CocoPoseKeypoints.RIGHT_SHOULDER.value] > 0.8
            and keypoints_scores[CocoPoseKeypoints.LEFT_HIP.value] > 0.8
            and keypoints_scores[CocoPoseKeypoints.RIGHT_HIP.value] > 0.8
        ):
            shoulder_mid = (keypoints[CocoPoseKeypoints.LEFT_SHOULDER.value] + keypoints[CocoPoseKeypoints.RIGHT_SHOULDER.value]) / 2
            hip_mid = (keypoints[CocoPoseKeypoints.LEFT_HIP.value] + keypoints[CocoPoseKeypoints.RIGHT_HIP.value]) / 2
            spine_vector = hip_mid - shoulder_mid
            self.spine_angle = np.degrees(np.arctan2(spine_vector[0], spine_vector[1]))
        else:
            self.spine_angle = 0.0

        if keypoints_scores[CocoPoseKeypoints.LEFT_WRIST.value] > 0.8 and keypoints_scores[CocoPoseKeypoints.RIGHT_WRIST.value] > 0.8:
            hand_center = (keypoints[CocoPoseKeypoints.LEFT_WRIST.value] + keypoints[CocoPoseKeypoints.RIGHT_WRIST.value]) / 2

            if self._hand_center_old is not None:
                alpha = 0.5
                self.hand_center_diff = (1 - alpha) * self.hand_center_diff + alpha * (hand_center - self._hand_center_old)
            self._hand_center_old = hand_center

            steering_vector = keypoints[CocoPoseKeypoints.LEFT_WRIST.value] - keypoints[CocoPoseKeypoints.RIGHT_WRIST.value]
            self.steering_angle = -math.degrees(math.atan2(steering_vector[1], steering_vector[0]))
            self.accelerate = True
        else:
            self._hand_center_old = None
            self.hand_center_diff = np.array([0.0, 0.0])

            self.steering_angle = 0.0
            self.accelerate = False

        if keypoints_scores[CocoPoseKeypoints.RIGHT_WRIST.value] > 0.8:
            if self._hand_right_old is not None:
                alpha = 0.3
                self.hand_right_diff = (1 - alpha) * self.hand_right_diff + alpha * (
                    keypoints[CocoPoseKeypoints.RIGHT_WRIST.value] - self._hand_right_old
                )
            self._hand_right_old = keypoints[CocoPoseKeypoints.RIGHT_WRIST.value]
        else:
            self._hand_right_old = None
            self.hand_right_diff = np.array([0.0, 0.0])

        swipe_threshold_in = 8
        swipe_threshold_out = 1

        if self.hand_right_diff[0] > swipe_threshold_in:
            self.swipe_left = True
        elif self.hand_right_diff[0] < swipe_threshold_out / 2:
            self.swipe_left = False

        if self.hand_right_diff[0] < -swipe_threshold_in:
            self.swipe_right = True
        elif self.hand_right_diff[0] > -swipe_threshold_out / 2:
            self.swipe_right = False

        if self.hand_right_diff[1] < -swipe_threshold_in:
            self.swipe_up = True
        elif self.hand_right_diff[1] > -swipe_threshold_out / 2:
            self.swipe_up = False

        if self.hand_right_diff[1] > swipe_threshold_in:
            self.swipe_down = True
        elif self.hand_right_diff[1] < swipe_threshold_out / 2:
            self.swipe_down = False
