"""Vote across frames and accept a plate only when the same text wins."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass


def normalize_text(text: str, allowed: str) -> str:
    return "".join(ch for ch in text.upper() if ch in allowed)


@dataclass
class PlateVote:
    track_id: int
    plate: str
    count: int
    total: int


class PlateVoter:
    def __init__(self, pattern: str, min_votes: int, allowed: str) -> None:
        self.pattern = re.compile(pattern)
        self.min_votes = min_votes
        self.allowed = allowed
        self.history: dict[int, list[str]] = {}
        self.locked: set[int] = set()

    def add(self, track_id: int, text: str) -> PlateVote | None:
        """Record one read. Return the plate once, when it first wins the vote."""
        cleaned = normalize_text(text, self.allowed)
        readings = self.history.setdefault(track_id, [])
        readings.append(cleaned)
        if track_id in self.locked:
            return None
        plate, count = Counter(readings).most_common(1)[0]
        if count < self.min_votes or self.pattern.fullmatch(plate) is None:
            return None
        self.locked.add(track_id)
        return PlateVote(track_id, plate, count, len(readings))

    def winners(self) -> list[PlateVote]:
        votes = []
        for track_id, readings in self.history.items():
            if not readings:
                continue
            plate, count = Counter(readings).most_common(1)[0]
            if count < self.min_votes or self.pattern.fullmatch(plate) is None:
                continue
            votes.append(PlateVote(track_id, plate, count, len(readings)))
        return votes
