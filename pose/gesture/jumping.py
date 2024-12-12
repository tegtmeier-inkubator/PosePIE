from dataclasses import dataclass

import numpy as np

from pose.gesture.base import GestureBase
from pose.keypoints import Keypoints
from utils.filter import Derivative, Ewma
from utils.vector import Vector2


@dataclass
class JumpingResult:
    detected: bool


class Jumping(GestureBase[JumpingResult]):
    def __init__(self) -> None:
        self._shoulder_width: float = 0.0
        self._hip_center_diff = Derivative()
        self._hip_center_ewma = Ewma(0.1)

        self._sensitivity: float = 0.4

    def set_sensitivity(self, sensitivity: float) -> None:
        self._sensitivity = sensitivity

    def set_shoulder_width(self, shoulder_width: float) -> None:
        self._shoulder_width = shoulder_width

    def parse_keypoints(self, keypoints: Keypoints) -> JumpingResult:
        if keypoints.left_hip.conf > 0.8 and keypoints.right_hip.conf > 0.8:
            hip_center = (keypoints.left_hip.xy + keypoints.right_hip.xy) / 2
            hip_center_diff = self._hip_center_ewma(self._hip_center_diff(hip_center))
        else:
            self._hip_center_diff.reset()
            self._hip_center_ewma.reset()
            hip_center_diff = np.array([0.0, 0.0])

        detected = Vector2(hip_center_diff).y < -self._shoulder_width / self._sensitivity

        return JumpingResult(detected)
