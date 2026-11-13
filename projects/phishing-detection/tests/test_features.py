import unittest
from features import extract_features

class FeatureTests(unittest.TestCase):
    def test_https_and_suspicious_terms_are_extracted(self):
        values = extract_features("https://account-verify.example.test/login")
        self.assertEqual(values["https"], 1.0)
        self.assertGreater(values["suspicious_term_count"], 0)

    def test_ip_host_is_flagged(self):
        values = extract_features("http://192.0.2.10/signin")
        self.assertEqual(values["host_is_ip"], 1.0)

    def test_empty_input_is_rejected(self):
        with self.assertRaises(ValueError):
            extract_features("")

    def test_missing_host_is_rejected(self):
        with self.assertRaises(ValueError):
            extract_features("https:///missing-host")

if __name__ == "__main__":
    unittest.main()
