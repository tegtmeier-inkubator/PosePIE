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

from dataclasses import dataclass
import os
from pathlib import Path

from typing import Any, Optional

import numpy as np
from pydantic import BaseModel, Field
from ultralytics import YOLO

from cv2.typing import MatLike
import numpy.typing as npt

from pose.person import Person
from pose.tracking import Tracking


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
        ge=0.0,
        le=1.0,
        description="minimum required confidence for detecting a person",
    )
    min_keypoint_conf: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="minimum required confidence for detecting a keypoint",
    )
    tracking_timeout: float = Field(
        default=4.0,
        ge=0.0,
        description="time in seconds until invisible person is unassined",
    )


@dataclass
class PosePlayerStats:
    track_id: int | None
    visible: bool
    timeout: float | None


@dataclass
class PoseStats:
    unassigned_track_ids: list[int]
    player_stats: list[PosePlayerStats]


@dataclass
class PoseFrameResult:
    result: Any
    stats: PoseStats


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


def filter_keypoints_at_edge(
    keypoints: npt.NDArray[np.float64],
    keypoints_scores: npt.NDArray[np.float64],
) -> npt.NDArray[np.float64]:
    keypoints_x_at_edge = keypoints[..., 0] % 1.0 == 0.0
    keypoints_y_at_edge = keypoints[..., 1] % 1.0 == 0.0
    keypoints_at_edge = keypoints_x_at_edge | keypoints_y_at_edge

    keypoints_scores[keypoints_at_edge] = 0.0

    return keypoints_scores


class PoseModel:
    def __init__(
        self,
        config: PoseModelConfig,
        max_num_persons: int = 4,
    ) -> None:
        self._config = config
        assert max_num_persons >= 1

        if self._config.tensorrt:
            if not os.path.exists(Path(self._config.model_path) / f"{self._config.model}.engine"):
                model_tmp = YOLO(Path(self._config.model_path) / f"{self._config.model}.pt")
                model_tmp.export(format="engine", simplify=True, half=True, batch=1)

            self._model = YOLO(Path(self._config.model_path) / f"{self._config.model}.engine")
        else:
            self._model = YOLO(Path(self._config.model_path) / f"{self._config.model}.pt")

        self._tracking = Tracking(max_num_persons, self._config.min_keypoint_conf, self._config.tracking_timeout)

        self.person = [Person(self._config.min_keypoint_conf) for _ in range(max_num_persons)]

    def process_frame(self, frame: MatLike) -> PoseFrameResult:
        results = self._model.track(
            frame,
            persist=True,
            imgsz=1280 if "-p6" in self._config.model else 640,
            conf=self._config.min_bbox_conf,
            device=self._config.device,
            verbose=False,
        )
        stats = self._parse_results(results[0], frame.shape)

        return PoseFrameResult(results[0], stats)

    def _parse_results(self, result: Any, frame_shape: tuple[int, int]) -> PoseStats:
        if result.boxes.conf is not None and result.boxes.id is not None and result.keypoints.conf is not None:
            bboxes = result.boxes.xyxyn.cpu().numpy()
            track_ids = result.boxes.id.int().cpu().tolist()
            keypoints = result.keypoints.xyn.cpu().numpy()
            keypoints_scores = result.keypoints.conf.cpu().numpy()

            keypoints_scores = filter_keypoints_at_edge(keypoints, keypoints_scores)
            bboxes, keypoints = correct_aspect_ratio(frame_shape, bboxes, keypoints)
        else:
            bboxes = np.empty((0, 4))
            track_ids = []
            keypoints = np.empty((0, 17, 2))
            keypoints_scores = np.empty((0, 17, 1))

        self._tracking.retire_tracks(track_ids)

        unassigned_track_ids = self._tracking.assign_tracks(track_ids, keypoints, keypoints_scores)

        player_stats: list[PosePlayerStats] = []
        for person_id, person in enumerate(self.person):
            try:
                track_id = self._tracking.person_to_track[person_id]
            except KeyError:
                person.parse_keypoints(np.zeros((17, 2)), np.zeros((17,)))
                player_stats.append(PosePlayerStats(track_id=None, visible=False, timeout=None))
                continue

            try:
                idx = track_ids.index(track_id)
            except ValueError:
                person.parse_keypoints(np.zeros((17, 2)), np.zeros((17,)))
                player_stats.append(PosePlayerStats(track_id, visible=False, timeout=self._tracking.get_track_timeout(track_id)))
                continue

            person.parse_keypoints(keypoints[idx], keypoints_scores[idx])
            player_stats.append(PosePlayerStats(track_id, visible=True, timeout=None))

        return PoseStats(unassigned_track_ids, player_stats)
