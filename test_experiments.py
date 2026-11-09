import unittest
import xml.etree.ElementTree as ET

from experiments import cache_cost, chart, replay_effects, scenarios


class PortfolioTests(unittest.TestCase):
    def test_reference_calculations(self):
        data = {item[0]: item[3] for item in scenarios()}
        self.assertEqual(len(data), 10)
        self.assertAlmostEqual(data["01-ledger"][6][1], 1.6128)
        self.assertEqual(data["02-faults"][10], (12, 36, 594))
        self.assertAlmostEqual(data["03-replay"][1][1], 1.38)
        self.assertEqual(data["04-views"][-1][1], 480)
        self.assertEqual(data["06-compaction"][0][2], 1152)
        self.assertEqual(data["07-workers"][4][1], 37.5)
        self.assertEqual(data["08-php"][4][1], 340)
        self.assertAlmostEqual(data["09-ssd"][0][1], 56.514, places=2)
        self.assertAlmostEqual(data["10-prefetch"][7][1], 2 / 1.2)

    def test_replay_counterexample(self):
        self.assertEqual(replay_effects(compact=False, fence=False), 1)
        self.assertEqual(replay_effects(compact=True, fence=False), 2)
        self.assertEqual(replay_effects(compact=True, fence=True), 1)

    def test_charts_and_reproducibility(self):
        self.assertEqual(cache_cost(12, True), cache_cost(12, True))
        for args in scenarios():
            with self.subTest(study=args[0]):
                root = ET.fromstring(chart(*args))
                self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")


if __name__ == "__main__":
    unittest.main()
