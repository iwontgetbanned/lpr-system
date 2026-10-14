"""Load YAML config and resolve paths from the repository root."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def _load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def _resolve(value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return (ROOT / path).resolve()


@dataclass
class Settings:
    device: int | str = 0
    imgsz: int = 640
    conf: float = 0.25
    iou: float = 0.7
    tracker: str = "bytetrack.yaml"
    weights: Path = field(default_factory=lambda: ROOT / "models" / "plate_detector.pt")
    ocr_every_n: int = 5
    min_votes: int = 3
    ocr_model: str = "cct-s-v2-global-model"
    allowed_chars: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    plate_regex: str = r"^[A-Z0-9]{4,8}$"
    source: str = ""


def load_settings() -> Settings:
    folder = ROOT / "configs"
    default = _load_yaml(folder / "default.yaml")
    ocr = _load_yaml(folder / "ocr.yaml")
    cameras = _load_yaml(folder / "cameras.yaml").get("cameras") or []
    source = ""
    if cameras:
        raw = cameras[0].get("source", "")
        source = str(raw)
        if source and not source.isdigit() and "://" not in source:
            source = str(_resolve(source))
    device = default.get("device", 0)
    if isinstance(device, str) and device.isdigit():
        device = int(device)
    return Settings(
        device=device,
        imgsz=int(default.get("imgsz", 640)),
        conf=float(default.get("conf", 0.25)),
        iou=float(default.get("iou", 0.7)),
        tracker=str(default.get("tracker", "bytetrack.yaml")),
        weights=_resolve(default.get("weights", "models/plate_detector.pt")),
        ocr_every_n=int(default.get("ocr_every_n", 5)),
        min_votes=int(default.get("min_votes", 3)),
        ocr_model=str(ocr.get("model", "cct-s-v2-global-model")),
        allowed_chars=str(ocr.get("allowed_chars", "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")),
        plate_regex=str(ocr.get("regex", r"^[A-Z0-9]{4,8}$")),
        source=source,
    )
