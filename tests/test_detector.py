"""Lane crop covers the near-stop-line region and boxes shift back to the full frame."""

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lpr.detection.detector import Detection
from lpr.detection.postprocess import lane_crop, shift_detections


class LaneCropTests(unittest.TestCase):
    def test_crop_matches_the_marked_lane(self):
        frame = np.zeros((1000, 2000, 3), dtype=np.uint8)
        lane, origin, zone = lane_crop(frame, (0.40, 0.50, 0.73, 0.70))
        self.assertEqual(origin, (800, 500))
        self.assertEqual(zone, (800, 500, 1460, 700))
        self.assertEqual(lane.shape, (200, 660, 3))

    def test_shift_puts_the_box_back_on_the_full_frame(self):
        detection = Detection(xyxy=(10, 20, 30, 40), conf=0.9, track_id=1)
        shifted = shift_detections([detection], (800, 500))
        self.assertEqual(shifted[0].xyxy, (810, 520, 830, 540))


if __name__ == "__main__":
    unittest.main()
