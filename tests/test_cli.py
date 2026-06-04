import unittest

from telegram_bot_health_checker.cli import exit_code_for_status, validate_token_format


class CliTests(unittest.TestCase):
    def test_exit_codes(self):
        self.assertEqual(exit_code_for_status("OK"), 0)
        self.assertEqual(exit_code_for_status("WARNING"), 1)
        self.assertEqual(exit_code_for_status("ERROR"), 2)

    def test_missing_token_is_error(self):
        result = validate_token_format("")
        self.assertIsNotNone(result)
        self.assertEqual(result.status, "ERROR")


if __name__ == "__main__":
    unittest.main()
