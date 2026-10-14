"""Detect, track, read every few frames, and keep the winning plate text."""

from __future__ import annotations

from lpr.config import Settings
from lpr.detection.detector import PlateDetector, detections_from_result
from lpr.detection.postprocess import lane_crop, shift_detections
from lpr.recognition.ocr import PlateReader
from lpr.recognition.validate import PlateVote, PlateVoter
from lpr.tracking.tracker import PlateTracker


def crop_box(frame, xyxy):
    height, width = frame.shape[:2]
    x1, y1, x2, y2 = (int(v) for v in xyxy)
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(width, x2), min(height, y2)
    if x2 <= x1 or y2 <= y1:
        return None
    return frame[y1:y2, x1:x2]


class Pipeline:
    def __init__(self, settings: Settings, detector=None, reader=None) -> None:
        self.settings = settings
        self.detector = detector or PlateDetector(settings)
        self.tracker = PlateTracker(self.detector)
        self.reader = reader or PlateReader(settings)
        self.voter = PlateVoter(settings.plate_regex, settings.min_votes, settings.allowed_chars)
        self.labels: dict[int, str] = {}
        self._seen: dict[int, int] = {}

    def process(self, frame) -> tuple[list[PlateVote], list, tuple[int, int, int, int]]:
        """Detect inside the lane crop. Boxes are returned in full-frame coordinates."""
        lane, origin, zone = lane_crop(frame, self.settings.crop)
        result = self.tracker.track_frame(lane)
        detections = shift_detections(detections_from_result(result), origin)
        locked: list[PlateVote] = []
        for detection in detections:
            if detection.track_id is None:
                continue
            count = self._seen.get(detection.track_id, 0) + 1
            self._seen[detection.track_id] = count
            if count % self.settings.ocr_every_n != 1:
                continue
            plate_crop = crop_box(frame, detection.xyxy)
            text = self.reader.read(plate_crop)
            if text:
                self.labels[detection.track_id] = text
            vote = self.voter.add(detection.track_id, text)
            if vote is None:
                continue
            self.labels[vote.track_id] = vote.plate
            locked.append(vote)
        return locked, detections, zone

    def winners(self) -> list[PlateVote]:
        return self.voter.winners()
