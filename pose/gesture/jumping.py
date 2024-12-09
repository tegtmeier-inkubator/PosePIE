from dataclasses import dataclass

import numpy as np

import numpy.typing as npt

from pose.gesture.base import GestureBase
from pose.keypoints import Keypoints
from utils.vector import Vector2


@dataclass
class JumpingResult:
    detected: bool


class Jumping(GestureBase[JumpingResult]):
    def __init__(self) -> None:
        self._hip_center_old: npt.NDArray[np.float64] | None = None
        self._hip_center_diff = np.array([0.0, 0.0])

        self._sensitivity: float = 0.01

    def set_sensitivity(self, sensitivity: float) -> None:
        self._sensitivity = sensitivity

    def parse_keypoints(self, keypoints: Keypoints) -> JumpingResult:
        if keypoints.left_hip.conf > 0.8 and keypoints.right_hip.conf > 0.8:
            hip_center = (keypoints.left_hip.xy + keypoints.right_hip.xy) / 2

            if self._hip_center_old is not None:
                alpha = 0.5
                self._hip_center_diff = (1 - alpha) * self._hip_center_diff + alpha * (hip_center - self._hip_center_old)
            self._hip_center_old = hip_center
        else:
            self._hip_center_old = None
            self._hip_center_diff = np.array([0.0, 0.0])

        detected = Vector2(self._hip_center_diff).y < -self._sensitivity

        return JumpingResult(detected)
