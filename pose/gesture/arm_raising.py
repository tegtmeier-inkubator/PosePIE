from dataclasses import dataclass

from pose.gesture.base import GestureBase
from pose.keypoints import Keypoints
from utils.side import Side


@dataclass
class ArmRaisingResult:
    detected: bool


class ArmRaising(GestureBase[ArmRaisingResult]):
    def __init__(self, side: Side):
        self._side = side

    def parse_keypoints(self, keypoints: Keypoints) -> ArmRaisingResult:
        if self._side is Side.LEFT:
            eye = keypoints.left_eye
            elbow = keypoints.left_elbow
        else:
            eye = keypoints.right_eye
            elbow = keypoints.right_elbow

        detected = elbow.conf > 0.8 and eye.conf > 0.8 and elbow.y < eye.y

        return ArmRaisingResult(detected)
