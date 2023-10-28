import os
import unittest
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from terminalgpt.main import cli


class TestLoadCommand(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.test_conversation_path = "test_conversations"
        os.makedirs(self.test_conversation_path, exist_ok=True)

    def tearDown(self):
        # Remove the test_conversations directory after the tests are done
        import shutil

        shutil.rmtree(self.test_conversation_path)

    def test_load_command_no_conversations(self):
        with patch(
            "terminalgpt.conversations.ConversationManager.get_conversations",
            MagicMock(return_value=[]),
        ):
            result = self.runner.invoke(cli, ["load"])
            self.assertIn("There are no conversations to load!", result.output)


if __name__ == "__main__":
    unittest.main()
