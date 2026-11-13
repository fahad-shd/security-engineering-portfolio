import unittest
from unittest.mock import Mock
from detector import inspect_process, load_signatures

class DetectorTests(unittest.TestCase):
    def setUp(self):
        self.signatures = load_signatures()

    def fake_process(self, **info):
        proc = Mock()
        proc.as_dict.return_value = {
            "pid": 123, "name": "keylogger.exe", "exe": "/opt/keylogger.exe",
            "cmdline": ["keylogger.exe", "--capture-keys"], "username": "tester",
            **info
        }
        return proc

    def test_matching_indicators_create_explainable_alert(self):
        result = inspect_process(self.fake_process(), self.signatures)
        self.assertIsNotNone(result)
        self.assertGreaterEqual(result["score"], self.signatures["alert_threshold"])
        self.assertTrue(result["reasons"])

    def test_benign_process_is_not_alerted(self):
        proc = self.fake_process(name="editor", exe="/usr/bin/editor",
                                 cmdline=["editor", "notes.txt"])
        self.assertIsNone(inspect_process(proc, self.signatures))

    def test_no_keyboard_data_is_collected(self):
        result = inspect_process(self.fake_process(), self.signatures)
        self.assertNotIn("keystrokes", result)
        self.assertNotIn("typed_text", result)

if __name__ == "__main__":
    unittest.main()
