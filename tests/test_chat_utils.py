"""Tests for chat_utils.py."""

import unittest

from terminalgpt import chat_utils


class TestChatUtils(unittest.TestCase):
    """Tests for chat_utils.py."""

    def set_test(self):
        """Sets a test."""

        messages = [
            {"role": "system", "content": "Hello user Hello user"},
            {"role": "user", "content": "Hello system Hello system"},
            {"role": "assistant", "content": "Hello user Hello user"},
            {"role": "user", "content": "Hello assistant Hello assistant"},
        ]
        return messages

    def test_exceeding_token_limit(self):
        """Tests exceeding_token_limit function."""

        self.assertTrue(chat_utils.exceeding_token_limit(1025, 1024))
        self.assertFalse(chat_utils.exceeding_token_limit(1000, 1023))

    def test_num_tokens_from_messages(self):
        """Tests num_tokens_from_messages function."""

        messages = self.set_test()
        self.assertEqual(chat_utils.num_tokens_from_messages(messages), 34)


if __name__ == "__main__":
    unittest.main()
