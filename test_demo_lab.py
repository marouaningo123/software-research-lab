import unittest

from run_lab import html_report, run


class DemoLabTests(unittest.TestCase):
    def test_all_studies_execute_and_render(self):
        reports = run()
        self.assertEqual([report["study"] for report in reports], list(range(1, 31)))
        self.assertEqual(reports, run())
        self.assertTrue(all(report["observations"] for report in reports))
        self.assertEqual(html_report(reports).count("<details>"), 30)

    def test_key_demonstrations(self):
        self.assertEqual(list(run(1)[0]["observations"].values()), [1, 2, 1])
        self.assertEqual(run(16)[0]["observations"]["assertions passed"], 2)
        observations = run(21)[0]["observations"]
        self.assertEqual(observations["confidence"]["unsupported"], 1)
        self.assertEqual(observations["evidence-aware"]["unsupported"], 0)
        self.assertTrue(run(27)[0]["observations"]["greedy parity"])
