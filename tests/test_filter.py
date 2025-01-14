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

import numpy as np

from utils.filter import Derivative, Ewma, FallingEdge, RisingEdge, Turbo


class TestEwma:
    def test_time_constant(self) -> None:
        ewma = Ewma(1.0)

        for i, timestamp in enumerate(np.linspace(0.0, 1.0, 60)):
            value = 1.0 if i != 0 else 0.0

            ewma_value = ewma(value, timestamp)

        np.testing.assert_approx_equal(ewma_value, 1 - (1 / np.e))

    def test_time_constant_zero(self) -> None:
        ewma = Ewma(0.0)

        for i, timestamp in enumerate(np.linspace(0.0, 1.0, 60)):
            value = 1.0 if i != 0 else 0.0

            ewma_value = ewma(value, timestamp)

            np.testing.assert_approx_equal(ewma_value, value)

    def test_time_constant_negative(self) -> None:
        ewma = Ewma(-1.0)

        for i, timestamp in enumerate(np.linspace(0.0, 1.0, 60)):
            value = 1.0 if i != 0 else 0.0

            ewma_value = ewma(value, timestamp)

            np.testing.assert_approx_equal(ewma_value, value)

    def test_no_time_difference(self) -> None:
        ewma = Ewma()

        value = ewma(0.0, timestamp=0.0)
        value = ewma(1.0, timestamp=0.0)

        np.testing.assert_approx_equal(value, 0.0)

    def test_without_timestamp(self) -> None:
        ewma = Ewma()

        value = ewma(0.0)
        value = ewma(1.0)

        assert value != 0.0

    def test_different_fps(self) -> None:
        ewma_60fps = Ewma()
        ewma_30fps = Ewma()
        ewma_15fps = Ewma()

        for i, timestamp in enumerate(np.linspace(0.0, 1.0, 60)):
            value = 1.0 if i != 0 else 0.0

            ewma_60fps_value = ewma_60fps(value, timestamp)

            if i % 2 == 0:
                ewma_30fps_value = ewma_30fps(value, timestamp)
                np.testing.assert_approx_equal(ewma_30fps_value, ewma_60fps_value)

            if i % 4 == 0:
                ewma_15fps_value = ewma_15fps(value, timestamp)
                np.testing.assert_approx_equal(ewma_15fps_value, ewma_60fps_value)


class TestDerivative:
    def test_derivative(self) -> None:
        derivative = Derivative()

        np.testing.assert_approx_equal(derivative(np.array([1.0]), timestamp=0.0), 0.0)
        np.testing.assert_approx_equal(derivative(np.array([1.0]), timestamp=1.0), 0.0)
        np.testing.assert_approx_equal(derivative(np.array([2.0]), timestamp=2.0), 1.0)
        np.testing.assert_approx_equal(derivative(np.array([2.5]), timestamp=3.0), 0.5)
        np.testing.assert_approx_equal(derivative(np.array([3.0]), timestamp=3.5), 1.0)

    def test_negative_values(self) -> None:
        derivative = Derivative()

        np.testing.assert_approx_equal(derivative(np.array([-1.0]), timestamp=0.0), 0.0)
        np.testing.assert_approx_equal(derivative(np.array([-1.0]), timestamp=1.0), 0.0)
        np.testing.assert_approx_equal(derivative(np.array([-2.0]), timestamp=2.0), -1.0)
        np.testing.assert_approx_equal(derivative(np.array([-2.5]), timestamp=3.0), -0.5)
        np.testing.assert_approx_equal(derivative(np.array([-3.0]), timestamp=3.5), -1.0)

    def test_negative_time(self) -> None:
        derivative = Derivative()

        np.testing.assert_approx_equal(derivative(np.array([1.0]), timestamp=0.0), 0.0)
        np.testing.assert_approx_equal(derivative(np.array([1.0]), timestamp=-1.0), 0.0)
        np.testing.assert_approx_equal(derivative(np.array([2.0]), timestamp=-2.0), -1.0)
        np.testing.assert_approx_equal(derivative(np.array([2.5]), timestamp=-3.0), -0.5)
        np.testing.assert_approx_equal(derivative(np.array([3.0]), timestamp=-3.5), -1.0)

    def test_no_time_difference(self) -> None:
        derivative = Derivative()

        np.testing.assert_approx_equal(derivative(np.array([1.0]), timestamp=0.0), 0.0)
        assert derivative(np.array([1.0]), timestamp=0.0) == 0.0
        assert np.isinf(derivative(np.array([2.0]), timestamp=0.0))

    def test_without_timestamp(self) -> None:
        derivative = Derivative()

        np.testing.assert_approx_equal(derivative(np.array([1.0])), 0.0)
        assert not np.isinf(derivative(np.array([2.0])))

    def test_different_fps(self) -> None:
        derivative_60fps = Derivative()
        derivative_30fps = Derivative()
        derivative_15fps = Derivative()

        for i, timestamp in enumerate(np.linspace(0.0, 1.0, 60)):
            value = 2 * timestamp

            derivative_60fps_value = derivative_60fps(value, timestamp)

            if i % 2 == 0:
                derivative_30fps_value = derivative_30fps(value, timestamp)
                np.testing.assert_approx_equal(derivative_30fps_value, derivative_60fps_value)

            if i % 4 == 0:
                derivative_15fps_value = derivative_15fps(value, timestamp)
                np.testing.assert_approx_equal(derivative_15fps_value, derivative_60fps_value)


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
