"""YOLO wrapper: load the plate detector and track boxes across frames."""

from __future__ import annotations

from dataclasses import dataclass

from lpr.config import Settings


@dataclass
class Detection:
    xyxy: tuple[float, float, float, float]
    conf: float
    track_id: int | None = None


def detections_from_result(result) -> list[Detection]:
    boxes = result.boxes
    if boxes is None or len(boxes) == 0:
        return []
    ids = boxes.id.int().cpu().tolist() if boxes.id is not None else [None] * len(boxes)
    detections = []
    for box, conf, track_id in zip(boxes.xyxy.cpu().tolist(), boxes.conf.cpu().tolist(), ids):
        detections.append(
            Detection(
                xyxy=(float(box[0]), float(box[1]), float(box[2]), float(box[3])),
                conf=float(conf),
                track_id=None if track_id is None else int(track_id),
            )
        )
    return detections


class PlateDetector:
    def __init__(self, settings: Settings) -> None:
        from ultralytics import YOLO

        if not settings.weights.exists():
            raise FileNotFoundError(f"Detector weights not found: {settings.weights}")
        self.settings = settings
        self.model = YOLO(str(settings.weights))

    def track(self, source):
        """Yield one result per frame, with ByteTrack ids when the detector sees a plate."""
        return self.model.track(
            source,
            persist=True,
            tracker=self.settings.tracker,
            device=self.settings.device,
            imgsz=self.settings.imgsz,
            conf=self.settings.conf,
            iou=self.settings.iou,
            stream=True,
            verbose=False,
        )
