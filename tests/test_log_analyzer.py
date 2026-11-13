import unittest
from tools.log_analyzer import analyze, parse_line

class LogAnalyzerTests(unittest.TestCase):
    def test_failed_and_success_sequence(self):
        lines = [
            "Nov 14 10:00:00 host sshd: Failed password for alice from 192.0.2.10 port 22 ssh2",
            "Nov 14 10:00:02 host sshd: Failed password for alice from 192.0.2.10 port 22 ssh2",
            "Nov 14 10:00:05 host sshd: Accepted password for alice from 192.0.2.10 port 22 ssh2",
        ]
        result = analyze(lines, threshold=2)
        self.assertEqual(result["parsed_events"], 3)
        self.assertEqual(result["sources_over_threshold"], ["192.0.2.10"])
        self.assertEqual(result["success_after_failures"][0]["prior_failures_in_file"], 2)

    def test_unrelated_line_is_ignored(self):
        self.assertIsNone(parse_line("system boot complete", 1))

if __name__ == "__main__":
    unittest.main()
