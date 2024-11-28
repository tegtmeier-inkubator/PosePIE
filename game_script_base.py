import os

from abc import ABC, abstractmethod

from ultralytics import YOLO

from input_emulation.gamepad import Gamepad
from pose.pose import Pose


class GameScriptBase(ABC):
    def __init__(self, max_num_players: int = 4):
        self.max_num_players = max_num_players

        self.pose = Pose(self.max_num_players)
        self.gamepad = [Gamepad() for _ in range(self.max_num_players)]

    def run(self) -> None:
        MODEL = "yolov8l-pose"

        if not os.path.exists(f"{MODEL}.engine"):
            model = YOLO(f"{MODEL}.pt")
            model.export(format="engine", simplify=True, half=True, batch=1)

        model = YOLO(f"{MODEL}.engine")
        results = model(source=3, show=True, save=False, conf=0.8, stream=True)

        for result in results:
            self.pose.parse(result)

            self.update()

            for gamepad in self.gamepad:
                gamepad.update()

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError
