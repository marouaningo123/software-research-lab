import unittest
from xml.etree import ElementTree

from wave2_experiments import chart, scenarios


class WaveTwoTests(unittest.TestCase):
    def test_reference_points(self):
        expected = [3.8, 3800, 500, 16, 10 / 3, 16384, 20, 100, 234.375, 3]
        studies = scenarios()
        self.assertEqual(len(studies), len(expected))
        for study, value in zip(studies, expected):
            with self.subTest(study=study[0]):
                self.assertAlmostEqual(study[3][-1][1], value)
                ElementTree.fromstring(chart(*study))
