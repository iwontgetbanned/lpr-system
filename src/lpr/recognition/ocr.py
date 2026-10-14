"""Read a plate crop with the fast-plate-ocr model."""

from __future__ import annotations

from lpr.config import Settings
from lpr.recognition.validate import normalize_text


class PlateReader:
    def __init__(self, settings: Settings) -> None:
        from fast_plate_ocr import LicensePlateRecognizer

        self.allowed = settings.allowed_chars
        self.reader = LicensePlateRecognizer(settings.ocr_model)

    def read(self, crop) -> str:
        if crop is None or crop.size == 0:
            return ""
        predictions = self.reader.run(crop)
        if not predictions:
            return ""
        plate = getattr(predictions[0], "plate", predictions[0])
        return normalize_text(str(plate), self.allowed)
