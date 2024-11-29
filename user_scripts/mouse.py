import uinput

from script.base import ScriptBase
from pose.keypoints import CocoPoseKeypoints


class Mouse(ScriptBase):
    def setup(self) -> None:
        self.max_num_players = 1

        self.mouse = uinput.Device([uinput.REL_X, uinput.REL_Y, uinput.BTN_LEFT, uinput.BTN_RIGHT])

    def update(self) -> None:
        right_hand_xy = self.pose.person[0].keypoints[CocoPoseKeypoints.RIGHT_WRIST]
        right_hand_center_offset_x = 0.5 - right_hand_xy[0]
        right_hand_center_offset_y = 0.5 - right_hand_xy[1]

        self.mouse.emit(uinput.REL_X, int(right_hand_center_offset_x * 100))
        self.mouse.emit(uinput.REL_Y, -int(right_hand_center_offset_y * 100))
