import numpy.typing as npt


class Vector2:
    def __init__(self, ndarray: npt.NDArray) -> None:
        assert ndarray.shape == (2,)

        self.x = ndarray[0]
        self.y = ndarray[1]

    def __repr__(self) -> str:
        return f"(x={self.x}, y={self.y})"
