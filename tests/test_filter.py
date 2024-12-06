import numpy as np

from utils.filter import Derivative, FallingEdge, RisingEdge, Turbo


class TestDerivative:
    def test_derivative(self) -> None:
        derivative = Derivative()

        assert derivative(np.array([1.0]), timestamp=0.0) == 0.0
        assert derivative(np.array([1.0]), timestamp=1.0) == 0.0
        assert derivative(np.array([2.0]), timestamp=2.0) == 1.0
        assert derivative(np.array([2.5]), timestamp=3.0) == 0.5
        assert derivative(np.array([3.0]), timestamp=3.5) == 1.0

    def test_negative_values(self) -> None:
        derivative = Derivative()

        assert derivative(np.array([-1.0]), timestamp=0.0) == 0.0
        assert derivative(np.array([-1.0]), timestamp=1.0) == 0.0
        assert derivative(np.array([-2.0]), timestamp=2.0) == -1.0
        assert derivative(np.array([-2.5]), timestamp=3.0) == -0.5
        assert derivative(np.array([-3.0]), timestamp=3.5) == -1.0

    def test_negative_time(self) -> None:
        derivative = Derivative()

        assert derivative(np.array([1.0]), timestamp=0.0) == 0.0
        assert derivative(np.array([1.0]), timestamp=-1.0) == 0.0
        assert derivative(np.array([2.0]), timestamp=-2.0) == -1.0
        assert derivative(np.array([2.5]), timestamp=-3.0) == -0.5
        assert derivative(np.array([3.0]), timestamp=-3.5) == -1.0

    def test_no_time_difference(self) -> None:
        derivative = Derivative()

        assert derivative(np.array([1.0]), timestamp=0.0) == 0.0
        assert np.isinf(derivative(np.array([2.0]), timestamp=0.0))

    def test_filter_coefficient(self) -> None:
        derivative = Derivative(filter_coefficient=0.9)

        assert derivative(np.array([1.0]), timestamp=0.0) == 0.00
        assert derivative(np.array([2.0]), timestamp=1.0) == 0.90
        assert derivative(np.array([3.0]), timestamp=2.0) == 0.99

    def test_without_timestamp(self) -> None:
        derivative = Derivative(filter_coefficient=0.9)

        assert derivative(np.array([1.0])) == 0.00
        assert not np.isinf(derivative(np.array([2.0])))


class TestRisingEdge:
    def test_start_with_false(self) -> None:
        rising_edge = RisingEdge()

        assert rising_edge(False) is False
        assert rising_edge(True) is True
        assert rising_edge(False) is False

    def test_start_with_true(self) -> None:
        rising_edge = RisingEdge()

        assert rising_edge(True) is False
        assert rising_edge(False) is False
        assert rising_edge(True) is True
        assert rising_edge(False) is False


class TestFallingEdge:
    def test_start_with_true(self) -> None:
        falling_edge = FallingEdge()

        assert falling_edge(True) is False
        assert falling_edge(False) is True
        assert falling_edge(True) is False

    def test_start_with_false(self) -> None:
        falling_edge = FallingEdge()

        assert falling_edge(False) is False
        assert falling_edge(True) is False
        assert falling_edge(False) is True
        assert falling_edge(True) is False


class TestTurbo:
    def test_interval(self) -> None:
        turbo = Turbo(1.0)

        assert turbo(True, timestamp=0.0) is True
        assert turbo(True, timestamp=0.0) is False
        assert turbo(True, timestamp=0.9) is False
        assert turbo(True, timestamp=1.0) is True

        assert turbo(False, timestamp=2.0) is False
        assert turbo(False, timestamp=2.5) is False

        assert turbo(True, timestamp=3.0) is True
        assert turbo(True, timestamp=3.0) is False
        assert turbo(True, timestamp=3.9) is False
        assert turbo(True, timestamp=4.0) is True

    def test_negative_time(self) -> None:
        turbo = Turbo(1.0)

        assert turbo(True, timestamp=-1.0) is True
        assert turbo(True, timestamp=-1.0) is False
        assert turbo(True, timestamp=-1.9) is False
        assert turbo(True, timestamp=-2.0) is False

    def test_without_timestamp(self) -> None:
        turbo = Turbo(1.0)

        assert turbo(True) is True
        assert turbo(True) is False
