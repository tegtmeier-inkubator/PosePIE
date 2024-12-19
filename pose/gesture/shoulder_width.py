from dataclasses import dataclass

import numpy as np

from pose.gesture.base import GestureBase
from pose.keypoints import Keypoints
from utils.filter import Ewma


@dataclass
class ShoulderWidthResult:
    detected: bool
    width: float


class ShoulderWidth(GestureBase[ShoulderWidthResult]):
    def __init__(self, min_keypoint_conf: float) -> None:
        self._min_keypoint_conf = min_keypoint_conf

        self._shoulder_width: float = 0.0
        self._shoulder_width_ewma = Ewma(0.5)

    def parse_keypoints(self, keypoints: Keypoints) -> ShoulderWidthResult:
        if keypoints.left_shoulder.conf > self._min_keypoint_conf and keypoints.right_shoulder.conf > self._min_keypoint_conf:
            shoulder_width = float(np.linalg.norm(keypoints.left_shoulder.xy - keypoints.right_shoulder.xy))
            self._shoulder_width = self._shoulder_width_ewma(shoulder_width)

            detected = True
        else:
            detected = False

        return ShoulderWidthResult(detected, self._shoulder_width)
