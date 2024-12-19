# Copyright (c) 2024 Daniel Stolpmann <dstolpmann@tegtmeier-inkubator.de>
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

from pose.gesture.shoulder_width import ShoulderWidth
from tests.utils.pose import Pose

MIN_KEYPOINT_CONF = 0.8


class TestShoulderWidth:
    def test_width(self) -> None:
        pose = Pose()
        shoulder_width = ShoulderWidth(MIN_KEYPOINT_CONF)

        result = shoulder_width.parse_keypoints(pose.keypoints)

        assert result.detected is True
        np.testing.assert_almost_equal(result.width, 0.4)

    def test_not_detected_keypoint_threshold(self) -> None:
        pose = Pose()
        shoulder_width = ShoulderWidth(MIN_KEYPOINT_CONF)

        pose.left_shoulder = np.array([0.7, 0.3, 0.5])
        pose.right_shoulder = np.array([0.3, 0.3, 0.5])
        result = shoulder_width.parse_keypoints(pose.keypoints)

        assert result.detected is False
        assert result.width == 0.0
