import time

import numpy as np

import numpy.typing as npt

from pose.keypoints import Keypoints


class Tracking:
    def __init__(self, max_num_persons: int, tracking_timeout: float) -> None:
        assert max_num_persons >= 1
        self._max_num_persons = max_num_persons
        self._tracking_timeout = tracking_timeout

        self._track_last_seen: dict[int, float] = {}

        self.person_to_track: dict[int, int] = {}

    def retire_tracks(
        self,
        track_ids: list[int],
        timestamp: float | None = None,
    ) -> None:
        if timestamp is None:
            timestamp = time.perf_counter()

        for track_id in track_ids:
            self._track_last_seen[track_id] = timestamp

        for track_id, last_seen in self._track_last_seen.copy().items():
            if timestamp - last_seen > self._tracking_timeout:
                del self._track_last_seen[track_id]
                self.person_to_track = {key: value for key, value in self.person_to_track.items() if value != track_id}

    def assign_tracks(
        self,
        track_ids: list[int],
        keypoints: npt.NDArray[np.float64],
        keypoints_scores: npt.NDArray[np.float64],
    ) -> list[int]:
        unassigned_track_ids = [track_id for track_id in track_ids if track_id not in self.person_to_track.values()]

        for track_id in unassigned_track_ids.copy():
            idx = track_ids.index(track_id)
            keypoints_person = Keypoints(keypoints[idx], keypoints_scores[idx])

            if (
                keypoints_person.right_elbow.conf > 0.8
                and keypoints_person.right_eye.conf > 0.8
                and keypoints_person.right_elbow.y < keypoints_person.right_eye.y
            ):
                for person_id in range(self._max_num_persons):
                    if person_id not in self.person_to_track:
                        self.person_to_track[person_id] = track_id
                        unassigned_track_ids.remove(track_id)
                        break

        return unassigned_track_ids
