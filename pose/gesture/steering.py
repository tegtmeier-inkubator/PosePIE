from dataclasses import dataclass
import math

import numpy as np

from pose.gesture.base import GestureBase
from pose.keypoints import Keypoints
from utils.vector import Vector2


@dataclass
class SteeringResult:
    detected: bool
    angle: float


class Steering(GestureBase[SteeringResult]):
    def __init__(self) -> None:
        self._shoulder_width: float = 0.0

    def parse_keypoints(self, keypoints: Keypoints) -> SteeringResult:
        if keypoints.left_shoulder.conf > 0.8 and keypoints.right_shoulder.conf > 0.8:
            shoulder_width = abs(keypoints.left_shoulder.x - keypoints.right_shoulder.x)
            alpha = 0.2 if self._shoulder_width > 0.0 else 1.0
            self._shoulder_width = alpha * shoulder_width + (1 - alpha) * self._shoulder_width

        if keypoints.left_wrist.conf > 0.8 and keypoints.right_wrist.conf > 0.8:
            steering_vector = Vector2(keypoints.left_wrist.xy - keypoints.right_wrist.xy)

            detected = bool(np.linalg.norm(steering_vector.xy) <= self._shoulder_width * 1.5)
            angle = -math.degrees(math.atan2(steering_vector.y, steering_vector.x)) if detected else 0.0
        else:
            detected = False
            angle = 0.0

        return SteeringResult(detected, angle)
