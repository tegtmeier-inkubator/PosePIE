import os

import numpy as np
from ultralytics import YOLO
import vgamepad as vg

from pose.keypoints import CocoPoseKeypoints


gamepad = vg.VX360Gamepad()

MODEL = "yolov8l-pose"

if not os.path.exists(f"{MODEL}.engine"):
    model = YOLO(f"{MODEL}.pt")
    model.export(format="engine", simplify=True, half=True, batch=1)

model = YOLO(f"{MODEL}.engine")
results = model(source=3, show=False, save=False, conf=0.5, stream=True)

for result in results:
    gamepad.reset()

    if result.keypoints.conf is not None:
        keypoints = result.keypoints.xy[0].cpu()
        conf = result.keypoints.conf[0].cpu()

        # spine_upper = np.mean([keypoints[CocoPoseKeypoints.LEFT_SHOULDER.value], keypoints[CocoPoseKeypoints.RIGHT_SHOULDER.value]], 0)
        # spine_lower = np.mean([keypoints[CocoPoseKeypoints.LEFT_HIP.value], keypoints[CocoPoseKeypoints.RIGHT_HIP.value]], 0)
        # spine = spine_upper - spine_lower

        # print(np.rad2deg(np.arctan2(spine[0], -spine[1])))

        if (
            np.min(
                [
                    conf[CocoPoseKeypoints.LEFT_WRIST.value],
                    conf[CocoPoseKeypoints.RIGHT_WRIST.value],
                ]
            )
            > 0.8
        ):
            left_wrist = keypoints[CocoPoseKeypoints.LEFT_WRIST.value]
            right_wrist = keypoints[CocoPoseKeypoints.RIGHT_WRIST.value]
            vector = left_wrist - right_wrist
            angle = float(-np.rad2deg(np.arctan2(vector[1], vector[0])))

            print(angle)

            gamepad.left_joystick_float(
                x_value_float=np.clip(angle / 90, -1, 1), y_value_float=0
            )
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)

    gamepad.update()
