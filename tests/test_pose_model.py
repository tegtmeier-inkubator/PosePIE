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
from pose.model import correct_aspect_ratio, filter_keypoints_at_edge


class TestCorrectAspectRatio:
    def test_landscape(self) -> None:
        bboxes, keypoints = correct_aspect_ratio(
            (1080, 1920),
            np.array([[0.0, 0.0, 1.0, 1.0]]),
            np.array([[[0.0, 0.0, 0.5], [1.0, 1.0, 0.5], [0.5, 0.5, 0.5]]]),
        )
        np.testing.assert_equal(bboxes, [[0.0, 0.21875, 1.0, 0.78125]])
        np.testing.assert_equal(keypoints, [[[0.0, 0.21875, 0.5], [1.0, 0.78125, 0.5], [0.5, 0.5, 0.5]]])

    def test_portrait(self) -> None:
        bboxes, keypoints = correct_aspect_ratio(
            (1920, 1080),
            np.array([[0.0, 0.0, 1.0, 1.0]]),
            np.array([[[0.0, 0.0, 0.5], [1.0, 1.0, 0.5], [0.5, 0.5, 0.5]]]),
        )
        np.testing.assert_equal(bboxes, [[0.21875, 0.0, 0.78125, 1.0]])
        np.testing.assert_equal(keypoints, [[[0.21875, 0.0, 0.5], [0.78125, 1.0, 0.5], [0.5, 0.5, 0.5]]])


class TestFilterKeypointsAtEdge:
    def test_filter(self) -> None:
        keypoints_scores = filter_keypoints_at_edge(
            np.array([[[0.5, 0.5], [0.0, 0.5], [0.5, 0.0], [1.0, 0.5], [0.5, 1.0]]]),
            np.array([[[0.5], [0.5], [0.5], [0.5], [0.5]]]),
        )
        np.testing.assert_equal(keypoints_scores, [[[0.5], [0.0], [0.0], [0.0], [0.0]]])
