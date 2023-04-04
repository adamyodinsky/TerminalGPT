"""Tests the chat loop."""

import json
import os
import shutil
import unittest
from unittest.mock import patch
import pexpect
from pexpect import TIMEOUT
import terminalgpt


class TestLoadCommandE2E(unittest.TestCase):
    """Tests for get_user_answer function."""

    def setUp(self):
        self.test_conversation_path = "test_conversations"
        os.makedirs(self.test_conversation_path, exist_ok=True)

    def tearDown(self):
        # Remove the test_conversations directory after the tests are done
        shutil.rmtree(self.test_conversation_path)

    def test_load_empty_e2e(self):
        """Tests the chat loop end-to-end."""

        # Set the executable path to your script containing the chat_loop function
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        _ = os.path.join(base_dir, "terminalgpt", "main.py")

        # Create a pexpect spawn object for your script
        with unittest.mock.patch(
            "terminalgpt.print_utils.print_markdown_slowly", print
        ):
            child = pexpect.spawn(
                "terminalgpt", timeout=10, args=["load"], encoding="utf-8"
            )

            # Expect the assistant's welcome message
            child.expect("There are no conversations to load!")


if __name__ == "__main__":
    unittest.main()
