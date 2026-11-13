import unittest
from tools.nmap_xml_report import summarize

SAMPLE = """<nmaprun><host><status state="up"/><address addr="192.0.2.20" addrtype="ipv4"/><ports><port protocol="tcp" portid="443"><state state="open"/><service name="https" product="Example" version="1.0"/></port></ports></host></nmaprun>"""

class NmapReportTests(unittest.TestCase):
    def test_extracts_host_and_service(self):
        report = summarize(SAMPLE)
        self.assertEqual(report["host_count"], 1)
        self.assertEqual(report["hosts"][0]["services"][0]["port"], 443)
        self.assertEqual(report["hosts"][0]["services"][0]["service"], "https")

if __name__ == "__main__":
    unittest.main()
