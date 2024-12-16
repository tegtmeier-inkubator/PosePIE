from abc import ABC, abstractmethod

import cv2
from ultralytics.utils.plotting import Annotator

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

PLAYER_COLORS = [
    (200, 0, 0),
    (0, 0, 200),
    (0, 200, 200),
    (0, 200, 0),
]


def get_player_color(player_id: int) -> tuple[int, int, int]:
    return PLAYER_COLORS[player_id % len(PLAYER_COLORS)]


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

    def add_mouse(self, absolute: bool = False) -> Mouse:
        mouse = Mouse(absolute)
        self._plugins.append(MousePlugin(mouse))
        return mouse

    def run(self) -> None:
        camera = Camera(self._config.camera)
        print(f"Opened camera with {camera.width}x{camera.height}@{camera.fps} ({camera.format_fourcc})")

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
                    annotator = Annotator(frame)

                    player_ids = (
                        {player.track_id: player_id for player_id, player in enumerate(pose_result.stats.player_stats)}
                        if pose_result.stats.player_stats is not None
                        else {}
                    )

                    for bbox, keypoints in zip(pose_result.result.boxes, pose_result.result.keypoints):
                        if bbox.id is None:
                            continue

                        track_id = int(bbox.id)

                        if track_id in player_ids:
                            annotator.kpts(keypoints.data[0])
                            annotator.box_label(
                                bbox.xyxy.squeeze(),
                                f"Player {player_ids[track_id] + 1}",
                                get_player_color(player_ids[track_id]),
                            )
                        else:
                            annotator.box_label(bbox.xyxy.squeeze())

                    joinable = True
                    for player_id, player in enumerate(pose_result.stats.player_stats):
                        if player.track_id:
                            if player.timeout is not None:
                                status = f"unassign in {player.timeout:.1f}s"
                            elif not player.visible:
                                status = "not visible"
                            else:
                                status = "assigned"
                        elif joinable:
                            status = "raise right arm to join"
                            joinable = False
                        else:
                            status = "not assigned"

                        height = 24.0
                        width = float(frame.shape[1]) / self.max_num_players
                        left = round(player_id * width)
                        right = round((player_id + 1) * width)
                        top = round(frame.shape[0] - height)
                        bottom = round(frame.shape[0])

                        cv2.rectangle(
                            frame,
                            (left, top),
                            (right, bottom),
                            get_player_color(player_id),
                            -1,
                        )

                        cv2.putText(
                            frame,
                            status,
                            (left + 8, top + 16),
                            cv2.FONT_HERSHEY_PLAIN,
                            1.0,
                            (255, 255, 255),
                        )

                    cv2.imshow(CV2_WINDOW_TITLE, frame)

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
