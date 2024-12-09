from dataclasses import dataclass
import math

from pose.gesture.base import GestureBase
from pose.keypoints import Keypoints
from utils.vector import Vector2


@dataclass
class SteeringResult:
    detected: bool
    angle: float


class Steering(GestureBase[SteeringResult]):
    def __init__(self) -> None:
        self.angle = 0.0

    def parse_keypoints(self, keypoints: Keypoints) -> SteeringResult:
        if keypoints.left_wrist.conf > 0.8 and keypoints.right_wrist.conf > 0.8:
            detected = True
            steering_vector = Vector2(keypoints.left_wrist.xy - keypoints.right_wrist.xy)
            angle = -math.degrees(math.atan2(steering_vector.y, steering_vector.x))
        else:
            detected = False
            angle = 0.0

        return SteeringResult(detected, angle)
