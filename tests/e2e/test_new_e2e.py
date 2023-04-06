"""Tests the chat loop."""

import os
import unittest

import pexpect
from pexpect import TIMEOUT


class TestNewCommandE2E(unittest.TestCase):
    """Tests for get_user_answer function."""

    def test_new_e2e(self):
        """Tests the chat loop end-to-end."""

        # Set the executable path to your script containing the chat_loop function
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        _ = os.path.join(base_dir, "terminalgpt", "main.py")

        # Create a pexpect spawn object for your script
        child = pexpect.spawn("terminalgpt", timeout=10, args=["new"], encoding="utf-8")

        # Expect the assistant's welcome message
        child.expect("Assistant:")

        # Send user input
        child.sendline("Hello")

        # Expect the assistant's response
        assert (
            child.expect("Assistant:", timeout=20) != TIMEOUT
        ), "Assistant did not respond"

        # Send 'exit' to end the chat loop
        child.sendline("exit")

        # Check if the script exits
        child.expect(pexpect.EOF)


if __name__ == "__main__":
    unittest.main()
