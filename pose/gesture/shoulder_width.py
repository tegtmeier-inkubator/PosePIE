from dataclasses import dataclass

import numpy as np

from pose.gesture.base import GestureBase
from pose.keypoints import Keypoints


@dataclass
class ShoulderWidthResult:
    detected: bool
    width: float


class ShoulderWidth(GestureBase[ShoulderWidthResult]):
    def __init__(self) -> None:
        self._shoulder_width: float = 0.0

    def parse_keypoints(self, keypoints: Keypoints) -> ShoulderWidthResult:
        if keypoints.left_shoulder.conf > 0.8 and keypoints.right_shoulder.conf > 0.8:
            shoulder_width = float(np.linalg.norm(keypoints.left_shoulder.xy - keypoints.right_shoulder.xy))
            alpha = 0.2 if self._shoulder_width > 0.0 else 1.0
            self._shoulder_width = alpha * shoulder_width + (1 - alpha) * self._shoulder_width

            detected = True
        else:
            detected = False

        return ShoulderWidthResult(detected, self._shoulder_width)
