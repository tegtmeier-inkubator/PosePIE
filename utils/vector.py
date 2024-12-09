import numpy as np

import numpy.typing as npt


class Vector2:
    def __init__(self, ndarray: npt.NDArray[np.float64]) -> None:
        assert ndarray.shape == (2,)

        self.xy = ndarray

    @property
    def x(self) -> float:
        return float(self.xy[0])

    @property
    def y(self) -> float:
        return float(self.xy[1])

    def __repr__(self) -> str:
        return f"(x={self.x}, y={self.y})"
