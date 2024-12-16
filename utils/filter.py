import time

from typing import overload

import numpy as np

import numpy.typing as npt


class Derivative:
    def __init__(self) -> None:
        self._old_timestamp: float | None = None
        self._old_value: npt.NDArray[np.float64] | float | None = None

    def reset(self) -> None:
        self._old_timestamp = None
        self._old_value = None

    @overload
    def __call__(self, value: npt.NDArray[np.float64], timestamp: float | None = None) -> npt.NDArray[np.float64]: ...
    @overload
    def __call__(self, value: float, timestamp: float | None = None) -> float: ...
    def __call__(self, value: npt.NDArray[np.float64] | float, timestamp: float | None = None) -> npt.NDArray[np.float64] | float:
        if timestamp is None:
            timestamp = time.perf_counter()

        if self._old_value is not None and self._old_timestamp is not None:
            time_diff = timestamp - self._old_timestamp
            diff = (
                (value - self._old_value) / (timestamp - self._old_timestamp)
                if not np.isclose(time_diff, 0.0)
                else np.full_like(value, np.inf) if isinstance(value, np.ndarray) else np.inf
            )
        else:
            diff = np.zeros_like(value) if isinstance(value, np.ndarray) else 0.0

        self._old_timestamp = timestamp
        self._old_value = value

        return diff


class Ewma:
    def __init__(self, time_constant: float = 1.0) -> None:
        self._time_constant = time_constant

        self._old_timestamp: float | None = None
        self._value: npt.NDArray[np.float64] | float | None = None

    def reset(self) -> None:
        self._old_timestamp = None
        self._value = None

    @overload
    def __call__(self, value: npt.NDArray[np.float64], timestamp: float | None = None) -> npt.NDArray[np.float64]: ...
    @overload
    def __call__(self, value: float, timestamp: float | None = None) -> float: ...
    def __call__(self, value: npt.NDArray[np.float64] | float, timestamp: float | None = None) -> npt.NDArray[np.float64] | float:
        if timestamp is None:
            timestamp = time.perf_counter()

        if self._value is None:
            self._value = value

        if self._old_timestamp is not None:
            time_diff = timestamp - self._old_timestamp

            alpha = float(1.0 - np.exp(-time_diff / self._time_constant)) if self._time_constant > 0.0 else 1.0
            self._value = alpha * value + (1 - alpha) * self._value

        self._old_timestamp = timestamp

        return self._value


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


class Turbo:
    def __init__(self, interval: float) -> None:
        self._interval = interval

        self._firing: bool = False
        self._last_fired: float = -np.inf

    def __call__(self, value: bool, timestamp: float | None = None) -> bool:
        if timestamp is None:
            timestamp = time.perf_counter()

        if self._firing:
            self._firing = False
        else:
            if value and timestamp - self._last_fired >= self._interval:
                self._firing = True
                self._last_fired = timestamp
            elif not value:
                self._last_fired = -np.inf

        return self._firing
