from dataclasses import dataclass

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

    def set_shoulder_width(self, shoulder_width: float) -> None:
        self._shoulder_width = shoulder_width

    def parse_keypoints(self, keypoints: Keypoints) -> SteeringResult:
        if keypoints.left_wrist.conf > 0.8 and keypoints.right_wrist.conf > 0.8:
            steering_vector = Vector2(keypoints.left_wrist.xy - keypoints.right_wrist.xy)

            detected = float(np.linalg.norm(steering_vector.xy)) < self._shoulder_width * 1.5
            angle = float(-np.degrees(np.atan2(steering_vector.y, steering_vector.x))) if detected else 0.0
        else:
            detected = False
            angle = 0.0

        return SteeringResult(detected, angle)
