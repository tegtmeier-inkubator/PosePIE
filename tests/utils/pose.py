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

import numpy.typing as npt

from pose.keypoints import Keypoints


class Pose:
    def __init__(self) -> None:
        self.nose = np.array([0.5, 0.1, 1.0])
        self.left_eye = np.array([0.55, 0.08, 1.0])
        self.right_eye = np.array([0.45, 0.08, 1.0])
        self.left_ear = np.array([0.6, 0.1, 1.0])
        self.right_ear = np.array([0.4, 0.1, 1.0])
        self.left_shoulder = np.array([0.7, 0.3, 1.0])
        self.right_shoulder = np.array([0.3, 0.3, 1.0])
        self.left_elbow = np.array([0.8, 0.3, 1.0])
        self.right_elbow = np.array([0.2, 0.3, 1.0])
        self.left_wrist = np.array([0.9, 0.3, 1.0])
        self.right_wrist = np.array([0.1, 0.3, 1.0])
        self.left_hip = np.array([0.6, 0.5, 1.0])
        self.right_hip = np.array([0.4, 0.5, 1.0])
        self.left_knee = np.array([0.6, 0.7, 1.0])
        self.right_knee = np.array([0.4, 0.7, 1.0])
        self.left_ankle = np.array([0.6, 0.9, 1.0])
        self.right_ankle = np.array([0.4, 0.9, 1.0])

    @property
    def bbox_xyxy(self) -> npt.NDArray[np.float64]:
        keypoints_xy = self.keypoints.xy

        return np.array(
            [
                np.min(keypoints_xy[:, 0]),
                np.min(keypoints_xy[:, 1]),
                np.max(keypoints_xy[:, 0]),
                np.max(keypoints_xy[:, 1]),
            ]
        )

    @property
    def keypoints(self) -> Keypoints:
        return Keypoints(
            np.array(
                [
                    self.nose[:2],
                    self.left_eye[:2],
                    self.right_eye[:2],
                    self.left_ear[:2],
                    self.right_ear[:2],
                    self.left_shoulder[:2],
                    self.right_shoulder[:2],
                    self.left_elbow[:2],
                    self.right_elbow[:2],
                    self.left_wrist[:2],
                    self.right_wrist[:2],
                    self.left_hip[:2],
                    self.right_hip[:2],
                    self.left_knee[:2],
                    self.right_knee[:2],
                    self.left_ankle[:2],
                    self.right_ankle[:2],
                ]
            ),
            np.array(
                [
                    self.nose[2],
                    self.left_eye[2],
                    self.right_eye[2],
                    self.left_ear[2],
                    self.right_ear[2],
                    self.left_shoulder[2],
                    self.right_shoulder[2],
                    self.left_elbow[2],
                    self.right_elbow[2],
                    self.left_wrist[2],
                    self.right_wrist[2],
                    self.left_hip[2],
                    self.right_hip[2],
                    self.left_knee[2],
                    self.right_knee[2],
                    self.left_ankle[2],
                    self.right_ankle[2],
                ]
            ),
        )
