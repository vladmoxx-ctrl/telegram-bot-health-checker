import unittest

from telegram_bot_health_checker.reporting import build_report, mask_token, redact_sensitive_text, CheckResult


class ReportingTests(unittest.TestCase):
    def test_mask_token(self):
        masked = mask_token("123456789:ABCDEF0123456789abcdef")
        self.assertNotIn("ABCDEF0123456789abcdef", masked)
        self.assertIn(":", masked)

    def test_redact_sensitive_text(self):
        text = "token=123456789:ABCDEF0123456789abcdef_ABCDEF"
        redacted = redact_sensitive_text(text)
        self.assertNotIn("ABCDEF0123456789abcdef", redacted)
        self.assertIn("<redacted-token>", redacted)

    def test_build_report_status(self):
        report = build_report([CheckResult("token", "OK", "ok")])
        self.assertEqual(report.status, "OK")

        report = build_report([CheckResult("webhook", "WARNING", "warning")])
        self.assertEqual(report.status, "WARNING")

        report = build_report([CheckResult("token", "ERROR", "error")])
        self.assertEqual(report.status, "ERROR")


if __name__ == "__main__":
    unittest.main()
