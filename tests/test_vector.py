import numpy as np
import pytest

from utils.vector import Vector2


class TestVector2:
    def test_members(self) -> None:
        vector = Vector2(np.array([1.0, 2.0]))

        assert vector.x == 1.0
        assert vector.y == 2.0
        np.testing.assert_equal(vector.xy, [1.0, 2.0])

    def test_invalid_input_dimension(self) -> None:
        with pytest.raises(AssertionError):
            _ = Vector2(np.array([1.0]))

        with pytest.raises(AssertionError):
            _ = Vector2(np.array([1.0, 2.0, 3.0]))

        with pytest.raises(AssertionError):
            _ = Vector2(np.array([[1.0], [2.0]]))

    def test_repr(self) -> None:
        vector = Vector2(np.array([1.0, 2.0]))

        assert repr(vector) == "(x=1.0, y=2.0)"
