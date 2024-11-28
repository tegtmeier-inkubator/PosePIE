from typing import Any

import numpy as np

from pose.person import Person


class Pose:
    def __init__(self, max_num_persons: int = 4) -> None:
        assert max_num_persons >= 1

        self.person = [Person() for _ in range(max_num_persons)]

    def parse(self, result: Any) -> None:
        if result.boxes.conf is not None and result.keypoints.conf is not None:
            bboxes = result.boxes.xyxy.cpu().numpy()
            keypoints = result.keypoints.xy.cpu().numpy()
            keypoints_scores = result.keypoints.conf.cpu().numpy()

            positions_x = [bbox[0] for bbox in bboxes]
            idxs = np.argsort(positions_x)[::-1]

            for person_id, person in enumerate(self.person):
                if person_id < len(idxs):
                    person.parse_keypoints(keypoints[idxs[person_id]], keypoints_scores[idxs[person_id]])

                    print(
                        f"Player {person_id+1}: {person.steering_angle} {person.spine_angle} {person.hand_center_diff} {person.hand_right_diff}"
                    )
                else:
                    print(f"Player {person_id+1}: Not visible")
