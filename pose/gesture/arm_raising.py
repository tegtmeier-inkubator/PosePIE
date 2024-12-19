from dataclasses import dataclass

from pose.gesture.base import GestureBase
from pose.keypoints import Keypoints
from utils.side import Side


@dataclass
class ArmRaisingResult:
    detected: bool


class ArmRaising(GestureBase[ArmRaisingResult]):
    def __init__(self, min_keypoint_conf: float, side: Side):
        self._min_keypoint_conf = min_keypoint_conf
        self._side = side

    def parse_keypoints(self, keypoints: Keypoints) -> ArmRaisingResult:
        if self._side is Side.LEFT:
            eye = keypoints.left_eye
            elbow = keypoints.left_elbow
        else:
            eye = keypoints.right_eye
            elbow = keypoints.right_elbow

        detected = elbow.conf > self._min_keypoint_conf and eye.conf > self._min_keypoint_conf and elbow.y < eye.y

        return ArmRaisingResult(detected)
