from dataclasses import dataclass

import numpy as np

import numpy.typing as npt

from pose.gesture.base import GestureBase
from pose.keypoints import Keypoints
from utils.filter import Ewma
from utils.side import Side


@dataclass
class PointingResult:
    detected: bool
    xy: npt.NDArray[np.float32]


class Pointing(GestureBase[PointingResult]):
    def __init__(self, side: Side):
        self._side = side

        self._shoulder_width: float = 0.0
        self._ratio = 16 / 9
        self._reference_shoulder_xy = np.array([0.0, 0.0])
        self._reference_shoulder_xy_ewma = Ewma(0.2)
        self._xy = np.array([0.0, 0.0])
        self._xy_ewma = Ewma(0.1)

    def set_aspect_ratio(self, aspect_radio: tuple[float, float]) -> None:
        self._ratio = aspect_radio[0] / aspect_radio[1]

    def set_shoulder_width(self, shoulder_width: float) -> None:
        self._shoulder_width = shoulder_width

    def parse_keypoints(self, keypoints: Keypoints) -> PointingResult:
        if self._side is Side.LEFT:
            reference_shoulder = keypoints.left_shoulder
            wrist = keypoints.left_wrist
        else:
            reference_shoulder = keypoints.right_shoulder
            wrist = keypoints.right_wrist

        if reference_shoulder.conf > 0.8:
            self._reference_shoulder_xy = self._reference_shoulder_xy_ewma(reference_shoulder.xy)

        detected = False
        if reference_shoulder.conf > 0.8 and wrist.conf > 0.8:
            xy = (wrist.xy - self._reference_shoulder_xy) / self._shoulder_width
            if self._ratio > 1.0:
                xy[1] *= self._ratio
            elif self._ratio < 1.0:
                xy[0] /= self._ratio

            if (np.abs(xy) < 1.25).all():
                xy = np.clip(xy, -1.0, 1.0)
                self._xy = self._xy_ewma(xy)

                detected = True
            else:
                self._xy_ewma.reset()
        else:
            self._xy_ewma.reset()

        return PointingResult(detected, self._xy)
