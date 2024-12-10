from dataclasses import dataclass

import numpy as np

from pose.gesture.base import GestureBase
from pose.keypoints import Keypoints
from utils.vector import Vector2


@dataclass
class LeaningResult:
    detected: bool
    angle: float


class Leaning(GestureBase[LeaningResult]):
    def __init__(self) -> None:
        self.angle = 0.0

    def parse_keypoints(self, keypoints: Keypoints) -> LeaningResult:
        if (
            keypoints.left_shoulder.conf > 0.8
            and keypoints.right_shoulder.conf > 0.8
            and keypoints.left_hip.conf > 0.8
            and keypoints.right_hip.conf > 0.8
        ):
            shoulder_mid_xy = (keypoints.left_shoulder.xy + keypoints.right_shoulder.xy) / 2
            hip_mid_xy = (keypoints.left_hip.xy + keypoints.right_hip.xy) / 2
            spine_vector = Vector2(hip_mid_xy - shoulder_mid_xy)

            detected = True
            angle = np.degrees(np.arctan2(spine_vector.x, spine_vector.y))
        else:
            detected = False
            angle = 0.0

        return LeaningResult(detected, angle)
