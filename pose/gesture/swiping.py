from dataclasses import dataclass

import numpy as np

import numpy.typing as npt

from pose.gesture.base import GestureBase
from pose.keypoints import Keypoints
from utils.side import Side
from utils.vector import Vector2


@dataclass
class SwipingResult:
    left: bool
    right: bool
    up: bool
    down: bool


class Swiping(GestureBase[SwipingResult]):
    def __init__(self, side: Side):
        self._side = side

        self._shoulder_width: float = 0.0
        self._position_old: npt.NDArray[np.float64] | None = None
        self._position_diff = np.array([0.0, 0.0])
        self._left: bool = False
        self._right: bool = False
        self._up: bool = False
        self._down: bool = False

    def set_shoulder_width(self, shoulder_width: float) -> None:
        self._shoulder_width = shoulder_width

    def parse_keypoints(self, keypoints: Keypoints) -> SwipingResult:
        if self._side is Side.LEFT:
            wrist = keypoints.left_wrist
        else:
            wrist = keypoints.right_wrist

        if wrist.conf > 0.8:
            if self._position_old is not None:
                alpha = 1.0
                self._position_diff = (1 - alpha) * self._position_diff + alpha * (wrist.xy - self._position_old)
            self._position_old = wrist.xy
        else:
            self._position_old = None
            self._position_diff = np.array([0.0, 0.0])

        swipe_threshold_in = self._shoulder_width / 4
        swipe_threshold_out = swipe_threshold_in / 4

        position_diff_vector = Vector2(self._position_diff)
        norm = np.linalg.norm(position_diff_vector.xy)
        angle = np.degrees(np.arctan2(-position_diff_vector.y, -position_diff_vector.x))

        if norm > swipe_threshold_in:
            self._left = bool(angle < -135 or angle > 135)
            self._right = bool(-45 < angle < 45)
            self._up = bool(45 < angle < 135)
            self._down = bool(-135 < angle < -45)
        elif norm < swipe_threshold_out:
            self._left = False
            self._right = False
            self._up = False
            self._down = False

        return SwipingResult(self._left, self._right, self._up, self._down)
