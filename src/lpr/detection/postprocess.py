"""Crop the lane out of a camera frame before plate detection."""

from __future__ import annotations

from lpr.detection.detector import Detection


def lane_crop(frame, fractions: tuple[float, float, float, float]):
    """Return the lane image, its top-left corner, and the full-frame rectangle.

    ``fractions`` is ``(x1, y1, x2, y2)`` as portions of the frame width and height.
    """
    height, width = frame.shape[:2]
    x1, y1, x2, y2 = fractions
    left = min(width - 1, max(0, int(width * x1)))
    top = min(height - 1, max(0, int(height * y1)))
    right = min(width, max(left + 1, int(width * x2)))
    bottom = min(height, max(top + 1, int(height * y2)))
    return frame[top:bottom, left:right], (left, top), (left, top, right, bottom)


def shift_detections(detections: list[Detection], origin: tuple[int, int]) -> list[Detection]:
    """Move boxes from crop coordinates back onto the full frame."""
    offset_x, offset_y = origin
    shifted = []
    for detection in detections:
        x1, y1, x2, y2 = detection.xyxy
        shifted.append(
            Detection(
                xyxy=(x1 + offset_x, y1 + offset_y, x2 + offset_x, y2 + offset_y),
                conf=detection.conf,
                track_id=detection.track_id,
            )
        )
    return shifted
