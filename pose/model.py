import os
from pathlib import Path

from typing import Any, Optional

import numpy as np
from pydantic import BaseModel, Field
from ultralytics import YOLO

from cv2.typing import MatLike
import numpy.typing as npt

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


def correct_aspect_ratio(
    frame_shape: tuple[int, int],
    bboxes: npt.NDArray,
    keypoints: npt.NDArray,
) -> tuple[npt.NDArray, npt.NDArray]:
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

        if self._config.tensorrt:
            if not os.path.exists(Path(self._config.model_path) / f"{self._config.model}.engine"):
                model_tmp = YOLO(Path(self._config.model_path) / f"{self._config.model}.pt")
                model_tmp.export(format="engine", simplify=True, half=True, batch=1)

            self._model = YOLO(Path(self._config.model_path) / f"{self._config.model}.engine")
        else:
            self._model = YOLO(Path(self._config.model_path) / f"{self._config.model}.pt")

        self.person = [Person() for _ in range(max_num_persons)]

    def process_frame(self, frame: MatLike) -> Any:
        results = self._model(
            frame,
            imgsz=1280 if "-p6" in self._config.model else 640,
            conf=self._config.min_bbox_conf,
            device=self._config.device,
        )
        self._parse_results(results[0], frame.shape)

        return results[0]

    def _parse_results(self, result: Any, frame_shape: tuple[int, int]) -> None:
        if result.boxes.conf is not None and result.keypoints.conf is not None:
            bboxes = result.boxes.xyxyn.cpu().numpy()
            keypoints = result.keypoints.xyn.cpu().numpy()
            keypoints_scores = result.keypoints.conf.cpu().numpy()

            bboxes, keypoints = correct_aspect_ratio(frame_shape, bboxes, keypoints)

            positions_x = [bbox[0] for bbox in bboxes]
            idxs = np.argsort(positions_x)[::-1]

            for person_id, person in enumerate(self.person):
                if person_id < len(idxs):
                    person.parse_keypoints(keypoints[idxs[person_id]], keypoints_scores[idxs[person_id]])

                    print(
                        f"Player {person_id+1}: {person.steering_angle} {person.spine_angle} {person.hand_center_diff} {person.hand_right_diff}"
                    )
                else:
                    print(f"Player {person_id+1}: Not visible")
