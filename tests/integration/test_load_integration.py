import json
import os
import shutil
import unittest
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from terminalgpt.main import cli


class TestLoadCommandIntegration(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.test_conversation_path = "test_conversations"
        os.makedirs(self.test_conversation_path, exist_ok=True)

    def tearDown(self):
        # Remove the test_conversations directory after the tests are done
        shutil.rmtree(self.test_conversation_path)

    def test_load_command_integration(self):
        file_name = "test_conversation"
        messages = [{"role": "user", "content": "Test message"}]

        with open(os.path.join(self.test_conversation_path, file_name), "w") as f:
            json.dump(messages, f)

        with patch(
            "terminalgpt.conversations.ConversationManager.get_conversations",
            MagicMock(return_value=[file_name]),
        ):
            result = self.runner.invoke(cli, args="load")

        self.assertIn(
            "Welcome back to TerminalGPT!",
            result.output,
        )

    def test_load_conv_nothing_to_load_integration(self):
        patch(
            "terminalgpt.conversations.ConversationManager.get_conversations",
            MagicMock(return_value=[]),
        )

        with patch(
            "terminalgpt.conversations.ConversationManager.get_conversations",
            MagicMock(return_value=[]),
        ):
            result = self.runner.invoke(cli, args="load")

            self.assertIn(
                "There are no conversations to load!",
                result.output,
            )


if __name__ == "__main__":
    unittest.main()
