from typing import Any, Callable, TypeVar, cast
import numpy as np

import numpy.typing as npt

from pose.gesture.arm_raising import ArmRaising, ArmRaisingResult
from pose.gesture.jumping import Jumping, JumpingResult
from pose.gesture.leaning import Leaning, LeaningResult
from pose.gesture.pointing import Pointing, PointingResult
from pose.gesture.shoulder_width import ShoulderWidth, ShoulderWidthResult
from pose.gesture.steering import Steering, SteeringResult
from pose.gesture.swiping import Swiping, SwipingResult
from pose.keypoints import Keypoints
from utils.side import Side

T = TypeVar("T")


class Person:
    def __init__(self) -> None:
        self.keypoints = Keypoints()

        self.cache: dict[Callable[..., Any], Any] = {}

        self._left_arm_raising = ArmRaising(Side.LEFT)
        self._right_arm_raising = ArmRaising(Side.RIGHT)
        self._jumping = Jumping()
        self._leaning = Leaning()
        self._left_hand_pointing = Pointing(Side.LEFT)
        self._right_hand_pointing = Pointing(Side.RIGHT)
        self._shoulder_width = ShoulderWidth()
        self._steering = Steering()
        self._left_hand_swiping = Swiping(Side.LEFT)
        self._right_hand_swiping = Swiping(Side.RIGHT)

    def parse_keypoints(
        self,
        keypoints: npt.NDArray[np.float64],
        keypoints_scores: npt.NDArray[np.float64],
    ) -> None:
        self.cache = {}

        self.keypoints = Keypoints(keypoints, keypoints_scores)

    @staticmethod
    def _cache(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(self: "Person") -> T:
            if func in self.cache:
                result = cast(T, self.cache[func])
            else:
                result = func(self)
                self.cache[func] = result

            return result

        return wrapper

    @property
    @_cache
    def left_arm_raising(self) -> ArmRaisingResult:
        return self._left_arm_raising.parse_keypoints(self.keypoints)

    @property
    @_cache
    def right_arm_raising(self) -> ArmRaisingResult:
        return self._right_arm_raising.parse_keypoints(self.keypoints)

    @property
    @_cache
    def jumping(self) -> JumpingResult:
        return self._jumping.parse_keypoints(self.keypoints)

    @property
    @_cache
    def leaning(self) -> LeaningResult:
        return self._leaning.parse_keypoints(self.keypoints)

    @property
    @_cache
    def left_hand_pointing(self) -> PointingResult:
        self._left_hand_pointing.set_shoulder_width(self.shoulder_width.width)

        return self._left_hand_pointing.parse_keypoints(self.keypoints)

    @property
    @_cache
    def right_hand_pointing(self) -> PointingResult:
        self._right_hand_pointing.set_shoulder_width(self.shoulder_width.width)

        return self._right_hand_pointing.parse_keypoints(self.keypoints)

    @property
    @_cache
    def shoulder_width(self) -> ShoulderWidthResult:
        return self._shoulder_width.parse_keypoints(self.keypoints)

    @property
    @_cache
    def steering(self) -> SteeringResult:
        self._steering.set_shoulder_width(self.shoulder_width.width)

        return self._steering.parse_keypoints(self.keypoints)

    @property
    @_cache
    def left_hand_swiping(self) -> SwipingResult:
        return self._left_hand_swiping.parse_keypoints(self.keypoints)

    @property
    @_cache
    def right_hand_swiping(self) -> SwipingResult:
        return self._right_hand_swiping.parse_keypoints(self.keypoints)
