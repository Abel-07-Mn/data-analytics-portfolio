import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from analyze import format_pct, pct


class MetricHelperTests(unittest.TestCase):
    def test_percentage_uses_supplied_denominator(self):
        self.assertAlmostEqual(pct(83, 166), 50.0)

    def test_zero_denominator_is_not_reported_as_zero_percent(self):
        self.assertIsNone(pct(0, 0))

    def test_percentage_format_is_consistent(self):
        self.assertEqual(format_pct(38.87), "38.9%")
        self.assertEqual(format_pct(None), "—")


if __name__ == "__main__":
    unittest.main()