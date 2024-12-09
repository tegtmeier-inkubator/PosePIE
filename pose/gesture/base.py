from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pose.keypoints import Keypoints

T = TypeVar("T")


class GestureBase(ABC, Generic[T]):
    @abstractmethod
    def parse_keypoints(self, keypoints: Keypoints) -> T:
        raise NotImplementedError
