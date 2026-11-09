import unittest
from xml.etree import ElementTree

from ai_experiments import chart, scenarios


class AIWaveTests(unittest.TestCase):
    def test_reference_values_and_svg(self):
        expected = [100 * (1 - 0.05 ** 0.001), 65, 90, 100, 16.777216,
                    0, 5, 0, 500, 4.096]
        self.assertEqual(len(scenarios()), len(expected))
        for scenario, value in zip(scenarios(), expected):
            with self.subTest(study=scenario[0]):
                self.assertAlmostEqual(scenario[3][-1][1], value)
                ElementTree.fromstring(chart(*scenario))
