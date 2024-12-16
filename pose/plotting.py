import cv2
from ultralytics.utils.plotting import Annotator

from cv2.typing import MatLike

from pose.model import PoseFrameResult


PLAYER_COLORS = [
    (200, 0, 0),
    (0, 0, 200),
    (0, 200, 200),
    (0, 200, 0),
]


def get_player_color(player_id: int) -> tuple[int, int, int]:
    return PLAYER_COLORS[player_id % len(PLAYER_COLORS)]


def annotate_frame(frame: MatLike, pose_result: PoseFrameResult, max_num_players: int) -> None:
    assert max_num_players >= 1

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
        width = float(frame.shape[1]) / max_num_players
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
