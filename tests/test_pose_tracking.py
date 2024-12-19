import numpy as np

from pose.tracking import Tracking
from tests.utils.pose import Pose

MIN_KEYPOINT_CONF = 0.8


class TestTracking:
    def test_tracking(self) -> None:
        pose1 = Pose()
        pose2 = Pose()
        pose3 = Pose()
        track_ids = []
        tracking = Tracking(4, MIN_KEYPOINT_CONF, 4.0)

        # Person 1 and 3 enter, but nobody raises hand
        track_ids = [1, 2]

        retired_track_ids = tracking.retire_tracks(track_ids, timestamp=1.0)
        unassigned_track_ids = tracking.assign_tracks(
            track_ids,
            np.array(
                [
                    pose1.keypoints.xy,
                    pose2.keypoints.xy,
                ]
            ),
            np.array(
                [
                    pose1.keypoints.conf,
                    pose2.keypoints.conf,
                ]
            ),
        )
        assert len(retired_track_ids) == 0
        assert len(unassigned_track_ids) == 2
        assert 1 in unassigned_track_ids
        assert 2 in unassigned_track_ids
        assert 0 not in tracking.person_to_track
        assert 1 not in tracking.person_to_track
        assert 2 not in tracking.person_to_track
        assert 3 not in tracking.person_to_track

        # Person 1 raises hand
        pose1.right_elbow = np.array([0.3, 0.05, 1.0])
        pose1.right_wrist = np.array([0.3, 0.00, 1.0])

        retired_track_ids = tracking.retire_tracks(track_ids, timestamp=2.0)
        unassigned_track_ids = tracking.assign_tracks(
            track_ids,
            np.array(
                [
                    pose1.keypoints.xy,
                    pose2.keypoints.xy,
                ]
            ),
            np.array(
                [
                    pose1.keypoints.conf,
                    pose2.keypoints.conf,
                ]
            ),
        )
        assert len(retired_track_ids) == 0
        assert len(unassigned_track_ids) == 1
        assert 2 in unassigned_track_ids
        assert 0 in tracking.person_to_track
        assert tracking.person_to_track[0] == 1
        assert 1 not in tracking.person_to_track
        assert 2 not in tracking.person_to_track
        assert 3 not in tracking.person_to_track

        pose1.right_elbow = np.array([0.2, 0.3, 1.0])
        pose1.right_wrist = np.array([0.1, 0.3, 1.0])

        # Person 2 raises hand
        pose2.right_elbow = np.array([0.3, 0.05, 1.0])
        pose2.right_wrist = np.array([0.3, 0.00, 1.0])

        retired_track_ids = tracking.retire_tracks(track_ids, timestamp=3.0)
        unassigned_track_ids = tracking.assign_tracks(
            track_ids,
            np.array(
                [
                    pose1.keypoints.xy,
                    pose2.keypoints.xy,
                ]
            ),
            np.array(
                [
                    pose1.keypoints.conf,
                    pose2.keypoints.conf,
                ]
            ),
        )
        assert len(retired_track_ids) == 0
        assert len(unassigned_track_ids) == 0
        assert 0 in tracking.person_to_track
        assert tracking.person_to_track[0] == 1
        assert 1 in tracking.person_to_track
        assert tracking.person_to_track[1] == 2
        assert 2 not in tracking.person_to_track
        assert 3 not in tracking.person_to_track

        pose2.right_elbow = np.array([0.2, 0.3, 1.0])
        pose2.right_wrist = np.array([0.1, 0.3, 1.0])

        # Person 1 disappears for less than 4 seconds
        track_ids.remove(1)

        retired_track_ids = tracking.retire_tracks(track_ids, timestamp=6.0)
        unassigned_track_ids = tracking.assign_tracks(
            track_ids,
            np.array(
                [
                    pose2.keypoints.xy,
                ]
            ),
            np.array(
                [
                    pose2.keypoints.conf,
                ]
            ),
        )
        assert len(retired_track_ids) == 0
        assert len(unassigned_track_ids) == 0
        assert 0 in tracking.person_to_track
        assert tracking.person_to_track[0] == 1
        np.testing.assert_approx_equal(tracking.get_track_timeout(tracking.person_to_track[0], timestamp=6.0), 1.0)
        assert 1 in tracking.person_to_track
        assert tracking.person_to_track[1] == 2
        np.testing.assert_approx_equal(tracking.get_track_timeout(tracking.person_to_track[1], timestamp=6.0), 4.0)
        assert 2 not in tracking.person_to_track
        assert 3 not in tracking.person_to_track

        # Person 1 disappears for more than 4 seconds
        retired_track_ids = tracking.retire_tracks(track_ids, timestamp=8.0)
        unassigned_track_ids = tracking.assign_tracks(
            track_ids,
            np.array(
                [
                    pose2.keypoints.xy,
                ]
            ),
            np.array(
                [
                    pose2.keypoints.conf,
                ]
            ),
        )
        assert len(retired_track_ids) == 1
        assert 1 in retired_track_ids
        assert len(unassigned_track_ids) == 0
        assert 0 not in tracking.person_to_track
        assert 1 in tracking.person_to_track
        assert tracking.person_to_track[1] == 2
        np.testing.assert_approx_equal(tracking.get_track_timeout(tracking.person_to_track[1], timestamp=8.0), 4.0)
        assert 2 not in tracking.person_to_track
        assert 3 not in tracking.person_to_track

        # Person 3 enteres and raises hand
        track_ids.append(3)
        pose3.right_elbow = np.array([0.3, 0.05, 1.0])
        pose3.right_wrist = np.array([0.3, 0.00, 1.0])

        retired_track_ids = tracking.retire_tracks(track_ids, timestamp=9.0)
        unassigned_track_ids = tracking.assign_tracks(
            track_ids,
            np.array(
                [
                    pose2.keypoints.xy,
                    pose3.keypoints.xy,
                ]
            ),
            np.array(
                [
                    pose2.keypoints.conf,
                    pose3.keypoints.conf,
                ]
            ),
        )
        assert len(retired_track_ids) == 0
        assert len(unassigned_track_ids) == 0
        assert 0 in tracking.person_to_track
        assert tracking.person_to_track[0] == 3
        assert 1 in tracking.person_to_track
        assert tracking.person_to_track[1] == 2
        assert 2 not in tracking.person_to_track
        assert 3 not in tracking.person_to_track

        pose3.right_elbow = np.array([0.2, 0.3, 1.0])
        pose3.right_wrist = np.array([0.1, 0.3, 1.0])
