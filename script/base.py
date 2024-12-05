from abc import ABC, abstractmethod

import cv2

from config import Config
from input_emulation.gamepad import Gamepad
from input_emulation.gamepad_plugin import GamepadPlugin
from input_emulation.keyboard import Keyboard
from input_emulation.keyboard_plugin import KeyboardPlugin
from input_emulation.mouse import Mouse
from input_emulation.mouse_plugin import MousePlugin
from pose.camera import Camera
from pose.model import PoseModel
from script.plugin import PluginBase

CV2_WINDOW_TITLE = "Camera"


class ScriptBase(ABC):
    def __init__(
        self,
        config: Config,
        max_num_players: int = 4,
    ) -> None:
        self._config = config
        self.max_num_players = max_num_players

        self._plugins: list[PluginBase] = []

        self.setup()

        self.pose = PoseModel(self._config.pose, self.max_num_players)

    def add_gamepad(self) -> Gamepad:
        gamepad = Gamepad()
        self._plugins.append(GamepadPlugin(gamepad))
        return gamepad

    def add_keyboard(self) -> Keyboard:
        keyboard = Keyboard()
        self._plugins.append(KeyboardPlugin(keyboard))
        return keyboard

    def add_mouse(self) -> Mouse:
        mouse = Mouse()
        self._plugins.append(MousePlugin(mouse))
        return mouse

    def run(self) -> None:
        camera = Camera(self._config.camera)

        try:
            for plugin in self._plugins:
                plugin.create()

            while camera.is_opened():
                frame = camera.read()
                if frame is None:
                    break

                pose_result = self.pose.process_frame(frame)

                for plugin in self._plugins:
                    plugin.pre_update()

                self.update()

                for plugin in self._plugins:
                    plugin.post_update()

                if self._config.show_camera:
                    annotated_frame = pose_result.plot()
                    cv2.imshow(CV2_WINDOW_TITLE, annotated_frame)

                    if cv2.waitKey(1) & 0xFF == ord("q") or not cv2.getWindowProperty(CV2_WINDOW_TITLE, cv2.WND_PROP_VISIBLE):
                        break
        except KeyboardInterrupt:
            pass

        for plugin in self._plugins:
            plugin.destroy()

        camera.release()
        cv2.destroyAllWindows()

    @abstractmethod
    def setup(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError
