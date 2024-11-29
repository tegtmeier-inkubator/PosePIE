import os

from abc import ABC, abstractmethod
from pathlib import Path

import cv2
from ultralytics import YOLO

from input_emulation.gamepad import Gamepad
from pose.pose import Pose

CAMERA_DEVICE = 3
DISPLAY_CAMERA = True
WINDOW_TITLE = "Camera"

POSE_MODELS_PATH = Path("models/pose")
POSE_MODEL = "yolov8l-pose"
MIN_BBOX_CONF = 0.8


class GameScriptBase(ABC):
    def __init__(self, max_num_players: int = 4):
        self.max_num_players = max_num_players

        self.setup()

        self.pose = Pose(self.max_num_players)
        self.gamepad = [Gamepad() for _ in range(self.max_num_players)]

    def run(self) -> None:
        if not os.path.exists(POSE_MODELS_PATH / f"{POSE_MODEL}.engine"):
            pose_model = YOLO(POSE_MODELS_PATH / f"{POSE_MODEL}.pt")
            pose_model.export(format="engine", simplify=True, half=True, batch=1)

        pose_model = YOLO(POSE_MODELS_PATH / f"{POSE_MODEL}.engine")
        cap = cv2.VideoCapture(CAMERA_DEVICE)

        try:
            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    break

                results = pose_model(frame, conf=MIN_BBOX_CONF)

                self.pose.parse(results[0])

                self.update()

                for gamepad in self.gamepad:
                    gamepad.update()

                if DISPLAY_CAMERA:
                    annotated_frame = results[0].plot()
                    cv2.imshow(WINDOW_TITLE, annotated_frame)

                    if cv2.waitKey(1) & 0xFF == ord("q") or not cv2.getWindowProperty(WINDOW_TITLE, cv2.WND_PROP_VISIBLE):
                        break
        except KeyboardInterrupt:
            pass

        cap.release()
        cv2.destroyAllWindows()

    @abstractmethod
    def setup(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError
