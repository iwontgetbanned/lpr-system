"""Run the plate loop on a video or camera and print one plate per track."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

os.environ.setdefault("OPENCV_FFMPEG_CAPTURE_OPTIONS", "rtsp_transport;tcp")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import cv2

from lpr.capture.stream import iter_frames
from lpr.config import load_settings
from lpr.pipeline import Pipeline
from lpr.utils.visualization import draw_tracks


def parse_args():
    parser = argparse.ArgumentParser(description="Read license plates from a video or camera.")
    parser.add_argument("--source", help="Video path, stream URL, or webcam index. Defaults to configs/cameras.yaml.")
    return parser.parse_args()


def resolve_source(raw: str):
    if raw.isdigit():
        return int(raw)
    path = Path(raw)
    if not path.is_file() and "://" not in raw:
        raise SystemExit(f"Source not found: {path}")
    return str(path) if path.is_file() else raw


def display_source(source) -> str:
    if not isinstance(source, str) or "://" not in source:
        return str(source)
    parts = urlsplit(source)
    if parts.username is None and parts.password is None:
        return source
    host = parts.hostname or ""
    if parts.port:
        host = f"{host}:{parts.port}"
    return urlunsplit((parts.scheme, host, parts.path, "", ""))


def main() -> None:
    args = parse_args()
    settings = load_settings()
    source = resolve_source(args.source or settings.source)
    pipeline = Pipeline(settings)
    print(f"Reading plates from {display_source(source)}")
    print("Press q in the video window to stop.")
    try:
        cv2.namedWindow("LPR", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("LPR", 1280, 720)
        for frame in iter_frames(source):
            locked, detections, zone = pipeline.process(frame)
            for vote in locked:
                print(f"track {vote.track_id}: {vote.plate} ({vote.count}/{vote.total})", flush=True)
            shown = draw_tracks(frame, detections, pipeline.labels, zone)
            cv2.imshow("LPR", shown)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
