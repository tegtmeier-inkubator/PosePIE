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

import time

import numpy as np

import numpy.typing as npt

from pose.person import Person


class Tracking:
    def __init__(self, max_num_persons: int, min_keypoint_conf: float, tracking_timeout: float) -> None:
        assert max_num_persons >= 1
        self._max_num_persons = max_num_persons
        self._min_keypoint_conf = min_keypoint_conf
        self._tracking_timeout = tracking_timeout

        self._track_last_seen: dict[int, float] = {}

        self.person_to_track: dict[int, int] = {}

    def retire_tracks(
        self,
        track_ids: list[int],
        timestamp: float | None = None,
    ) -> list[int]:
        if timestamp is None:
            timestamp = time.perf_counter()

        for track_id in track_ids:
            self._track_last_seen[track_id] = timestamp

        retired_track_ids: list[int] = []
        for track_id, last_seen in self._track_last_seen.copy().items():
            if timestamp - last_seen > self._tracking_timeout:
                retired_track_ids.append(track_id)
                del self._track_last_seen[track_id]
                self.person_to_track = {key: value for key, value in self.person_to_track.items() if value != track_id}

        return retired_track_ids

    def assign_tracks(
        self,
        track_ids: list[int],
        keypoints: npt.NDArray[np.float64],
        keypoints_scores: npt.NDArray[np.float64],
    ) -> list[int]:
        unassigned_track_ids = [track_id for track_id in track_ids if track_id not in self.person_to_track.values()]

        for track_id in unassigned_track_ids.copy():
            idx = track_ids.index(track_id)

            person = Person(self._min_keypoint_conf)
            person.parse_keypoints(keypoints[idx], keypoints_scores[idx])

            if person.right_arm_raising.detected:
                for person_id in range(self._max_num_persons):
                    if person_id not in self.person_to_track:
                        self.person_to_track[person_id] = track_id
                        unassigned_track_ids.remove(track_id)
                        break

        return unassigned_track_ids

    def get_track_timeout(
        self,
        track_id: int,
        timestamp: float | None = None,
    ) -> float:
        if timestamp is None:
            timestamp = time.perf_counter()

        return self._tracking_timeout - (timestamp - self._track_last_seen[track_id])
