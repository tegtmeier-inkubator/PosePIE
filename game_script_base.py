import os

from abc import ABC, abstractmethod

import cv2
from ultralytics import YOLO

from input_emulation.gamepad import Gamepad
from pose.pose import Pose

WINDOW_TITLE = "Camera"

CAMERA_DEVICE = 3
DISPLAY_CAMERA = True


class GameScriptBase(ABC):
    def __init__(self, max_num_players: int = 4):
        self.max_num_players = max_num_players

        self.setup()

        self.pose = Pose(self.max_num_players)
        self.gamepad = [Gamepad() for _ in range(self.max_num_players)]

    def run(self) -> None:
        MODEL = "yolov8l-pose"

        if not os.path.exists(f"{MODEL}.engine"):
            model = YOLO(f"{MODEL}.pt")
            model.export(format="engine", simplify=True, half=True, batch=1)

        model = YOLO(f"{MODEL}.engine")
        cap = cv2.VideoCapture(CAMERA_DEVICE)

        try:
            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    break

                results = model(frame, conf=0.8)

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
