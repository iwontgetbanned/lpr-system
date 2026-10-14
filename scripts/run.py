"""Run the plate loop on a video or camera and print one plate per track."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lpr.config import load_settings
from lpr.pipeline import Pipeline


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


def main() -> None:
    args = parse_args()
    settings = load_settings()
    source = resolve_source(args.source or settings.source)
    pipeline = Pipeline(settings)
    print(f"Reading plates from {source}")
    for result in pipeline.frames(source):
        pipeline.observe(result)
    winners = pipeline.winners()
    if not winners:
        print("No stable plate.")
        return
    for vote in winners:
        print(f"track {vote.track_id}: {vote.plate} ({vote.count}/{vote.total})")


if __name__ == "__main__":
    main()
