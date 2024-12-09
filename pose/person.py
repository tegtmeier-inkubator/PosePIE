import numpy as np

import numpy.typing as npt

from pose.gesture.arm_raising import ArmRaising, ArmRaisingResult
from pose.gesture.jumping import Jumping, JumpingResult
from pose.gesture.leaning import Leaning, LeaningResult
from pose.gesture.steering import Steering, SteeringResult
from pose.gesture.swiping import Swiping, SwipingResult
from pose.keypoints import Keypoints
from utils.side import Side


class Person:
    def __init__(self) -> None:
        self.keypoints = Keypoints()

        self._left_arm_raising = ArmRaising(Side.LEFT)
        self._right_arm_raising = ArmRaising(Side.RIGHT)
        self._jumping = Jumping()
        self._leaning = Leaning()
        self._steering = Steering()
        self._left_hand_swiping = Swiping(Side.LEFT)
        self._right_hand_swiping = Swiping(Side.RIGHT)

    def parse_keypoints(
        self,
        keypoints: npt.NDArray[np.float64],
        keypoints_scores: npt.NDArray[np.float64],
    ) -> None:
        self.keypoints = Keypoints(keypoints, keypoints_scores)

    @property
    def left_arm_raising(self) -> ArmRaisingResult:
        return self._left_arm_raising.parse_keypoints(self.keypoints)

    @property
    def right_arm_raising(self) -> ArmRaisingResult:
        return self._right_arm_raising.parse_keypoints(self.keypoints)

    @property
    def jumping(self) -> JumpingResult:
        return self._jumping.parse_keypoints(self.keypoints)

    @property
    def leaning(self) -> LeaningResult:
        return self._leaning.parse_keypoints(self.keypoints)

    @property
    def steering(self) -> SteeringResult:
        return self._steering.parse_keypoints(self.keypoints)

    @property
    def left_hand_swiping(self) -> SwipingResult:
        return self._left_hand_swiping.parse_keypoints(self.keypoints)

    @property
    def right_hand_swiping(self) -> SwipingResult:
        return self._right_hand_swiping.parse_keypoints(self.keypoints)
