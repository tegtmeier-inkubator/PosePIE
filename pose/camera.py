import cv2
from pydantic import BaseModel, Field

from cv2.typing import MatLike


class CameraConfig(BaseModel):
    device: int = Field(
        0,
        ge=0,
        description="device ID of camera",
    )


class Camera:
    def __init__(self, config: CameraConfig):
        self._config = config

        self._cap = cv2.VideoCapture(self._config.device)

    def is_opened(self) -> bool:
        return self._cap.isOpened()

    def read(self) -> MatLike | None:
        success, frame = self._cap.read()

        return frame if success else None

    def release(self) -> None:
        self._cap.release()
