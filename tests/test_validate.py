"""Plate votes accept a repeated matching string and drop a one-off blank."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lpr.recognition.validate import PlateVoter

PATTERN = r"^[A-Z0-9]{4,8}$"
ALLOWED = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


class PlateVoterTests(unittest.TestCase):
    def test_majority_wins(self):
        voter = PlateVoter(PATTERN, min_votes=3, allowed=ALLOWED)
        for _ in range(3):
            voter.add(9, "esz107")
        voter.add(9, "ESZ1O7")
        winners = voter.winners()
        self.assertEqual(len(winners), 1)
        self.assertEqual(winners[0].plate, "ESZ107")
        self.assertEqual(winners[0].count, 3)
        self.assertEqual(winners[0].total, 4)

    def test_add_returns_the_plate_once(self):
        voter = PlateVoter(PATTERN, min_votes=3, allowed=ALLOWED)
        self.assertIsNone(voter.add(9, "ESZ107"))
        self.assertIsNone(voter.add(9, "ESZ107"))
        locked = voter.add(9, "ESZ107")
        self.assertIsNotNone(locked)
        self.assertEqual(locked.plate, "ESZ107")
        self.assertIsNone(voter.add(9, "ESZ107"))

    def test_blank_and_single_read_are_dropped(self):
        voter = PlateVoter(PATTERN, min_votes=3, allowed=ALLOWED)
        voter.add(46, "")
        voter.add(5, "5PNA08")
        self.assertEqual(voter.winners(), [])


if __name__ == "__main__":
    unittest.main()
