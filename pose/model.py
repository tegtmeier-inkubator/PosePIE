import os
import time
from pathlib import Path

from typing import Any, Optional

import numpy as np
from pydantic import BaseModel, Field
from ultralytics import YOLO

from cv2.typing import MatLike
import numpy.typing as npt

from pose.keypoints import Keypoints
from pose.person import Person


class PoseModelConfig(BaseModel):
    model: str = Field(
        default="yolov8l-pose",
        description="name of Ultralytics pose model (e.g. yolov8l-pose, yolov8n-pose, yolo11l-pose)",
    )
    model_path: str = Field(
        default="models/pose",
        description="path to models folder",
    )
    tensorrt: bool = Field(
        default=False,
        description="use TensorRT for inference",
    )
    device: Optional[str] = Field(
        default=None,
        description="device to use for inference (e.g. cpu, cuda, cuda:0)",
    )
    min_bbox_conf: float = Field(
        default=0.8,
        description="minimum required confidence for detecting a person",
    )
    tracking_timeout: float = Field(
        default=4.0,
        description="time in seconds until invisible person is unassined",
    )


def correct_aspect_ratio(
    frame_shape: tuple[int, int],
    bboxes: npt.NDArray[np.float64],
    keypoints: npt.NDArray[np.float64],
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    if frame_shape[1] > frame_shape[0]:
        aspect_ratio = frame_shape[0] / frame_shape[1]
        shift = (1 - aspect_ratio) / 2
        bboxes[:, 1] = (bboxes[:, 1] * aspect_ratio) + shift
        bboxes[:, 3] = (bboxes[:, 3] * aspect_ratio) + shift
        keypoints[:, :, 1] = (keypoints[:, :, 1] * aspect_ratio) + shift
    else:
        aspect_ratio = frame_shape[1] / frame_shape[0]
        shift = (1 - aspect_ratio) / 2
        bboxes[:, 0] = (bboxes[:, 0] * aspect_ratio) + shift
        bboxes[:, 2] = (bboxes[:, 2] * aspect_ratio) + shift
        keypoints[:, :, 0] = (keypoints[:, :, 0] * aspect_ratio) + shift

    return bboxes, keypoints


class PoseModel:
    def __init__(
        self,
        config: PoseModelConfig,
        max_num_persons: int = 4,
    ) -> None:
        self._config = config
        assert max_num_persons >= 1

        self._person_to_track: dict[int, int] = {}
        self._track_last_seen: dict[int, float] = {}

        if self._config.tensorrt:
            if not os.path.exists(Path(self._config.model_path) / f"{self._config.model}.engine"):
                model_tmp = YOLO(Path(self._config.model_path) / f"{self._config.model}.pt")
                model_tmp.export(format="engine", simplify=True, half=True, batch=1)

            self._model = YOLO(Path(self._config.model_path) / f"{self._config.model}.engine")
        else:
            self._model = YOLO(Path(self._config.model_path) / f"{self._config.model}.pt")

        self.person = [Person() for _ in range(max_num_persons)]

    def process_frame(self, frame: MatLike) -> Any:
        results = self._model.track(
            frame,
            persist=True,
            imgsz=1280 if "-p6" in self._config.model else 640,
            conf=self._config.min_bbox_conf,
            device=self._config.device,
        )
        self._parse_results(results[0], frame.shape)

        return results[0]

    def _retire_tracks(
        self,
        track_ids: list[int],
        timestamp: float | None = None,
    ) -> None:
        if timestamp is None:
            timestamp = time.perf_counter()

        for track_id in track_ids:
            self._track_last_seen[track_id] = timestamp

        for track_id, last_seen in self._track_last_seen.copy().items():
            if timestamp - last_seen > self._config.tracking_timeout:
                del self._track_last_seen[track_id]
                self._person_to_track = {key: value for key, value in self._person_to_track.items() if value != track_id}

    def _assign_tracks(
        self,
        track_ids: list[int],
        keypoints: npt.NDArray[np.float64],
        keypoints_scores: npt.NDArray[np.float64],
    ) -> list[int]:
        unassigned_track_ids = [track_id for track_id in track_ids if track_id not in self._person_to_track.values()]

        for track_id in unassigned_track_ids.copy():
            idx = track_ids.index(track_id)
            keypoints_person = Keypoints(keypoints[idx], keypoints_scores[idx])

            if (
                keypoints_person.right_elbow.conf > 0.8
                and keypoints_person.right_eye.conf > 0.8
                and keypoints_person.right_elbow.y < keypoints_person.right_eye.y
            ):
                for person_id, _ in enumerate(self.person):
                    if person_id not in self._person_to_track:
                        self._person_to_track[person_id] = track_id
                        unassigned_track_ids.remove(track_id)
                        break

        return unassigned_track_ids

    def _parse_results(self, result: Any, frame_shape: tuple[int, int]) -> None:
        if result.boxes.conf is not None and result.boxes.id is not None and result.keypoints.conf is not None:
            bboxes = result.boxes.xyxyn.cpu().numpy()
            track_ids = result.boxes.id.int().cpu().tolist()
            keypoints = result.keypoints.xyn.cpu().numpy()
            keypoints_scores = result.keypoints.conf.cpu().numpy()

            bboxes, keypoints = correct_aspect_ratio(frame_shape, bboxes, keypoints)
        else:
            bboxes = np.empty((0, 4))
            track_ids = []
            keypoints = np.empty((0, 17, 2))
            keypoints_scores = np.empty((0, 17, 1))

        self._retire_tracks(track_ids)

        unassigned_track_ids = self._assign_tracks(track_ids, keypoints, keypoints_scores)
        print(f"Unassigned tracks: {unassigned_track_ids}")

        for person_id, person in enumerate(self.person):
            try:
                track_id = self._person_to_track[person_id]
            except KeyError:
                print(f"Player {person_id+1}: not assigned")
                person.parse_keypoints(np.zeros((17, 2)), np.zeros((17,)))
                break

            try:
                idx = track_ids.index(track_id)
            except ValueError:
                print(f"Player {person_id+1}: assigned to track {track_id} - not visible")
                person.parse_keypoints(np.zeros((17, 2)), np.zeros((17,)))
                break

            print(f"Player {person_id+1}: assigned to track {track_id} - {bboxes[idx]}")
            person.parse_keypoints(keypoints[idx], keypoints_scores[idx])
