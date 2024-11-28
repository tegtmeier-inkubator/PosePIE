import os

import numpy as np
from ultralytics import YOLO
import vgamepad as vg

from pose.player import Player


MODEL = "yolov8l-pose"

if not os.path.exists(f"{MODEL}.engine"):
    model = YOLO(f"{MODEL}.pt")
    model.export(format="engine", simplify=True, half=True, batch=1)

model = YOLO(f"{MODEL}.engine")
results = model(source=3, show=True, save=False, conf=0.8, stream=True)

gamepads = [vg.VX360Gamepad() for _ in range(4)]
pose_players = [Player() for _ in range(4)]

for result in results:
    for gamepad in gamepads:
        gamepad.reset()

    if result.boxes.conf is not None and result.keypoints.conf is not None:
        bboxes = result.boxes.xyxy.cpu().numpy()
        keypoints = result.keypoints.xy.cpu().numpy()
        keypoints_scores = result.keypoints.conf.cpu().numpy()

        positions_x = [bbox[0] for bbox in bboxes]
        idxs = np.argsort(positions_x)[::-1]

        for player_id, pose_player in enumerate(pose_players):
            pose_player.reset()

            if player_id < len(idxs):
                pose_player.parse_keypoints(keypoints[idxs[player_id]], keypoints_scores[idxs[player_id]])

                gamepads[player_id].left_joystick_float(
                    x_value_float=np.clip(pose_player.steering_angle / 90, -1, 1),
                    y_value_float=0,
                )

                if pose_player.accelerate:
                    gamepads[player_id].press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)

                print(
                    f"Player {player_id+1}: {pose_player.steering_angle} {pose_player.spine_angle} {pose_player.hand_center_diff} {pose_player.hand_right_diff}"
                )

    for gamepad in gamepads:
        gamepad.update()
