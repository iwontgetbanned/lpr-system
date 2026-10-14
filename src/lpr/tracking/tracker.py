"""Run ByteTrack through the plate detector, one frame at a time."""

from __future__ import annotations

from lpr.detection.detector import PlateDetector


class PlateTracker:
    def __init__(self, detector: PlateDetector) -> None:
        self.detector = detector

    def track_frame(self, frame):
        return self.detector.track_frame(frame)
