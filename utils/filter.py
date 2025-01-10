# Copyright (c) 2024, 2025 Daniel Stolpmann <dstolpmann@tegtmeier-inkubator.de>
#
# This file is part of PosePIE.
#
# PosePIE is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# PosePIE is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with PosePIE. If
# not, see <https://www.gnu.org/licenses/>.

import time

from typing import overload

import numpy as np

import numpy.typing as npt


class Derivative:
    """Derivative filter

    Computes the time derivative between the last and the current value.
    The class stores the last value internally, so a separate instance has to be used for each use of the filter.

    >>> derivative = Derivative()
    >>> derivative(1.0, timestamp = 0.0)
    0.0
    >>> derivative(2.0, timestamp = 1.0)
    1.0
    """

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
    """Exponentially Weighted Moving Average (EWMA) filter

    Performs low pass filtering of a value.
    The class stores the smoothed value internally, so a separate instance has to be used for each use of the filter.

    :param time_constant: time in seconds after which the smoothed signal of a unit step function reaches 1-1/e = 63.2%.

    >>> ewma = Ewma(time_constant = 1.0)
    >>> ewma(0.0, timestamp = 0.0)
    0.0
    >>> ewma(1.0, timestamp = 0.0)
    0.0
    >>> ewma(1.0, timestamp = 1.0)
    0.6321205588285577
    """

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
    """Rising edge filter

    Returns True if the input value switched from False to True and False otherwise.
    The class stores the last value internally, so a separate instance has to be used for each use of the filter.

    >>> rising_edge = RisingEdge()
    >>> rising_edge(True)
    False
    >>> rising_edge(False)
    False
    >>> rising_edge(True)
    True
    """

    def __init__(self) -> None:
        self._old_value = True

    def __call__(self, value: bool) -> bool:
        rising = (not self._old_value) and value
        self._old_value = value
        return rising


class FallingEdge:
    """Falling edge filter

    Returns True if the input value switched from True to False and False otherwise.
    The class stores the last value internally, so a separate instance has to be used for each use of the filter.

    >>> falling_edge = FallingEdge()
    >>> falling_edge(False)
    False
    >>> falling_edge(True)
    False
    >>> falling_edge(False)
    True
    """

    def __init__(self) -> None:
        self._old_value = False

    def __call__(self, value: bool) -> bool:
        falling = self._old_value and (not value)
        self._old_value = value
        return falling


class Turbo:
    """Turbo fire filter

    Returns True for a single call at a configurable interval as long as the input value is True.
    It always returns True when the input value became True and False if the input value is False.
    The class stores the state and a timer internally, so a separate instance has to be used for each use of the filter.

    :param interval: Interval in seconds in which the function returns single instances of True.

    >>> turbo = Turbo(interval = 1.0)
    >>> turbo(True, timestamp=0.0)
    True
    >>> turbo(True, timestamp=0.5)
    False
    >>> turbo(True, timestamp=1.0)
    True
    """

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
