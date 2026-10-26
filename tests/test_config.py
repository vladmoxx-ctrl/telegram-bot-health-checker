import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from telegram_bot_health_checker.config import build_config, load_dotenv

ROOT = Path(__file__).resolve().parents[1]


def config_from(text: str, **overrides):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / ".env"
        path.write_text(text, encoding="utf-8")
        options = dict(env_path=path, token=None, admin_chat_id=None, output_dir="reports", timeout=5.0, delete_webhook=False, send_admin_message=True)
        options.update(overrides)
        return build_config(**options)


class ConfigTests(unittest.TestCase):
    def setUp(self):
        # The process environment must not leak into these checks.
        names = ("TELEGRAM_BOT_TOKEN", "BOT_TOKEN", "TELEGRAM_ADMIN_CHAT_ID", "TELEGRAM_CHAT_ID", "ADMIN_CHAT_ID")
        patcher = mock.patch.dict(os.environ, {name: "" for name in names})
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_load_dotenv(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ".env"
            path.write_text("# comment\nTELEGRAM_BOT_TOKEN=123:abc\nEMPTY=\n", encoding="utf-8")
            values = load_dotenv(path)
            self.assertEqual(values["TELEGRAM_BOT_TOKEN"], "123:abc")
            self.assertEqual(values["EMPTY"], "")

    def test_env_example_is_understood(self):
        config = build_config(env_path=ROOT / ".env.example", token=None, admin_chat_id=None, output_dir="reports", timeout=5.0, delete_webhook=False, send_admin_message=True)
        self.assertTrue(config.token.startswith("123456789:"))
        self.assertEqual(config.admin_chat_id, "123456789")

    def test_preferred_names(self):
        config = config_from("TELEGRAM_BOT_TOKEN=1:new\nBOT_TOKEN=1:old\nTELEGRAM_ADMIN_CHAT_ID=7\nTELEGRAM_CHAT_ID=8\n")
        self.assertEqual(config.token, "1:new")
        self.assertEqual(config.admin_chat_id, "7")

    def test_other_common_names(self):
        config = config_from("BOT_TOKEN=1:old\nADMIN_CHAT_ID=9\n")
        self.assertEqual(config.token, "1:old")
        self.assertEqual(config.admin_chat_id, "9")
        config = config_from("TELEGRAM_BOT_TOKEN=1:x\nTELEGRAM_CHAT_ID=-1001\n")
        self.assertEqual(config.admin_chat_id, "-1001")

    def test_empty_value_falls_through(self):
        config = config_from("TELEGRAM_BOT_TOKEN=\nBOT_TOKEN=1:fallback\nTELEGRAM_ADMIN_CHAT_ID=\n")
        self.assertEqual(config.token, "1:fallback")
        self.assertIsNone(config.admin_chat_id)

    def test_command_line_wins(self):
        config = config_from("TELEGRAM_BOT_TOKEN=1:file\nTELEGRAM_CHAT_ID=8\n", token="1:cli", admin_chat_id="5")
        self.assertEqual(config.token, "1:cli")
        self.assertEqual(config.admin_chat_id, "5")

    def test_file_wins_over_process_environment(self):
        with mock.patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "1:process"}):
            self.assertEqual(config_from("BOT_TOKEN=1:file\n").token, "1:file")
            self.assertEqual(config_from("OTHER=1\n").token, "1:process")


if __name__ == "__main__":
    unittest.main()
