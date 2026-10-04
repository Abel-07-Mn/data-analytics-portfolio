import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from analyze import pct, segment


class AttritionMetricTests(unittest.TestCase):
    def test_pct_returns_none_for_empty_segment(self):
        self.assertIsNone(pct(0, 0))

    def test_segment_keeps_both_rate_and_denominator(self):
        rows = [
            {"Attrition": "Yes", "Department": "Sales"},
            {"Attrition": "No", "Department": "Sales"},
            {"Attrition": "No", "Department": "R&D"},
        ]
        result = {row["segment"]: row for row in segment(rows, "Department")}
        self.assertEqual(result["Sales"]["employees"], 2)
        self.assertEqual(result["Sales"]["leavers"], 1)
        self.assertEqual(result["Sales"]["attrition_rate_pct"], 50.0)


if __name__ == "__main__":
    unittest.main()