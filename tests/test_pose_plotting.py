import numpy as np

from pose.plotting import get_player_color


class TestPlayerColor:
    def test_player_color(self) -> None:
        np.testing.assert_equal(get_player_color(0), (200, 0, 0))
        np.testing.assert_equal(get_player_color(1), (0, 0, 200))
        np.testing.assert_equal(get_player_color(2), (0, 200, 200))
        np.testing.assert_equal(get_player_color(3), (0, 200, 0))
        np.testing.assert_equal(get_player_color(4), (200, 0, 0))
        np.testing.assert_equal(get_player_color(5), (0, 0, 200))
        np.testing.assert_equal(get_player_color(6), (0, 200, 200))
        np.testing.assert_equal(get_player_color(7), (0, 200, 0))
