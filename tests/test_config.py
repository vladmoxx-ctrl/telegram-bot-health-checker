import tempfile
import unittest
from pathlib import Path

from telegram_bot_health_checker.config import load_dotenv


class ConfigTests(unittest.TestCase):
    def test_load_dotenv(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ".env"
            path.write_text("# comment\nTELEGRAM_BOT_TOKEN=123:abc\nEMPTY=\n", encoding="utf-8")
            values = load_dotenv(path)
            self.assertEqual(values["TELEGRAM_BOT_TOKEN"], "123:abc")
            self.assertEqual(values["EMPTY"], "")


if __name__ == "__main__":
    unittest.main()
