import time

import numpy as np
import numpy.typing as npt


class Derivative:
    def __init__(self, filter_coefficient: float = 1.0) -> None:
        self._filter_coefficient = filter_coefficient

        self._diff = np.empty((0,))

        self._old_timestamp: float | None = None
        self._old_value: npt.NDArray | None = None

    def __call__(self, value: npt.NDArray, timestamp: float | None = None) -> npt.NDArray:
        if timestamp is None:
            timestamp = time.perf_counter()

        if self._diff.shape == (0,):
            self._diff = np.zeros_like(value)

        if self._old_value is not None and self._old_timestamp is not None:
            diff = (value - self._old_value) / (timestamp - self._old_timestamp)
            self._diff = (1 - self._filter_coefficient) * self._diff + self._filter_coefficient * diff

        self._old_timestamp = timestamp
        self._old_value = value

        return self._diff


class RisingEdge:
    def __init__(self) -> None:
        self._old_value = True

    def __call__(self, value: bool) -> bool:
        rising = (not self._old_value) and value
        self._old_value = value
        return rising


class FallingEdge:
    def __init__(self) -> None:
        self._old_value = False

    def __call__(self, value: bool) -> bool:
        falling = self._old_value and (not value)
        self._old_value = value
        return falling
