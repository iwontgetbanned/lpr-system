"""Draw plate boxes and the current text on a frame."""

from __future__ import annotations

import cv2


def draw_tracks(frame, detections, labels: dict | None = None, zone: tuple[int, int, int, int] | None = None):
    canvas = frame.copy()
    labels = labels or {}
    if zone is not None:
        x1, y1, x2, y2 = zone
        cv2.rectangle(canvas, (x1, y1), (x2, y2), (0, 0, 255), 2)
    for detection in detections:
        x1, y1, x2, y2 = (int(value) for value in detection.xyxy)
        track_id = detection.track_id
        text = labels.get(track_id, "") if track_id is not None else ""
        if text and track_id is not None:
            text = f"{track_id} {text}"
        elif not text:
            text = f"{detection.conf:.2f}"
        cv2.rectangle(canvas, (x1, y1), (x2, y2), (40, 200, 80), 2)
        cv2.putText(
            canvas,
            text,
            (x1, max(20, y1 - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (40, 200, 80),
            2,
            cv2.LINE_AA,
        )
    return canvas
