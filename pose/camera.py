import sys

from typing import Optional

import cv2
from pydantic import BaseModel, Field

from cv2.typing import MatLike


class CameraConfig(BaseModel):
    device: int = Field(
        default=0,
        ge=0,
        description="device ID of camera",
    )
    format_fourcc: Optional[str] = Field(
        default=None,
        min_length=4,
        max_length=4,
        description="capture format (FourCC)",
    )
    width: Optional[int] = Field(
        default=None,
        ge=0,
        description="capture width",
    )
    height: Optional[int] = Field(
        default=None,
        ge=0,
        description="capture height",
    )
    fps: Optional[int] = Field(
        default=None,
        ge=0,
        description="capture frames per second",
    )


class Camera:
    def __init__(self, config: CameraConfig):
        self._config = config

        self._cap = cv2.VideoCapture(self._config.device)
        if self._config.format_fourcc is not None:
            self._cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*self._config.format_fourcc.upper()))
        if self._config.width is not None:
            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._config.width)
        if self._config.height is not None:
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._config.height)
        if self._config.fps is not None:
            self._cap.set(cv2.CAP_PROP_FPS, self._config.fps)

        self.format_fourcc = int(self._cap.get(cv2.CAP_PROP_FOURCC)).to_bytes(4, byteorder=sys.byteorder).decode()
        self.width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self._cap.get(cv2.CAP_PROP_FPS))

    def is_opened(self) -> bool:
        return self._cap.isOpened()

    def read(self) -> MatLike | None:
        success, frame = self._cap.read()

        return frame if success else None

    def release(self) -> None:
        self._cap.release()
