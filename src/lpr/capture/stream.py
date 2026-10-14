"""Read frames from a video file, webcam, or RTSP camera."""

from __future__ import annotations

import cv2


def iter_frames(source):
    """Yield BGR frames. A live stream is retried briefly instead of stopping on one miss."""
    live = isinstance(source, str) and "://" in str(source)
    capture = cv2.VideoCapture(source)
    if not capture.isOpened():
        raise RuntimeError(f"Could not open video source: {source}")
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    misses = 0
    try:
        while True:
            ok, frame = capture.read()
            if not ok or frame is None:
                if not live or misses > 50:
                    break
                misses += 1
                continue
            misses = 0
            yield frame
    finally:
        capture.release()
