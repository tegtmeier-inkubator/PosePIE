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
from pose.plotting import annotate_frame
from script.plugin import PluginBase

CV2_WINDOW_TITLE = "PosePIE"


class ScriptBase(ABC):
    def __init__(
        self,
        config: Config,
        max_num_players: int = 4,
    ) -> None:
        self._config = config

        self.max_num_players = max_num_players
        """Maximum number of players

        Has to be set in the `setup()` method in the user script to define the maximum number of players that are handled by the program.
        Can be used in the `update()` method for a loop like `for player_id in range(self.max_num_players):` to iterate over all players.
        """

        self._plugins: list[PluginBase] = []

        self.setup()

        self.pose = PoseModel(self._config.pose, self.max_num_players)

    def add_gamepad(self) -> Gamepad:
        """Adds a virtual gamepad for input emulation"""
        gamepad = Gamepad()
        self._plugins.append(GamepadPlugin(gamepad))
        return gamepad

    def add_keyboard(self) -> Keyboard:
        """Adds a virtual keyboard for input emulation"""
        keyboard = Keyboard()
        self._plugins.append(KeyboardPlugin(keyboard))
        return keyboard

    def add_mouse(self, absolute: bool = False) -> Mouse:
        """Adds a virtual mouse for input emulation

        The mouse can operate in two modes.
        In relative mode, the mouse can be moved relative to its current position via the `move_relative` member.
        In absolute mode, the mouse can be moved absolute to normalized screen coordinates via the `move_absolute` member.

        :param absolute: whether absolute mode should be used
        """
        mouse = Mouse(absolute)
        self._plugins.append(MousePlugin(mouse))
        return mouse

    def run(self) -> None:
        """Main loop of the program

        This function should never be called in the user script.
        """
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
                    annotate_frame(frame, pose_result, self.max_num_players)
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
        """Setup of the user script

        This method is called once when the program starts and should define variables and set up the required emulated input devices.
        Here, `self.max_num_players` should be set to the maximum number of players.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """Update of the user script

        This method is executed at every frame and should contain the main mapping logic.
        The logic has to handle each player separately, which can be simplified by using a for loop up to the maximum number of players.
        """
        raise NotImplementedError
