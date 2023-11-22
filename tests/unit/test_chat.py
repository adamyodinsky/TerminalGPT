"""Tests for chat_utils.py."""

import unittest
from unittest.mock import MagicMock, patch

import openai
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style as PromptStyle

from terminalgpt import config
from terminalgpt.chat import ChatManager
from terminalgpt.conversations import ConversationManager
from terminalgpt.printer import PrinterFactory


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

        printer = PrinterFactory.get_printer("markdown")
        conv_manager = ConversationManager(printer=printer, client=MagicMock())

        session = PromptSession(
            style=PromptStyle.from_dict({"prompt": "bold"}),
            message="\nUser: ",
        )

        chat_manager = ChatManager(
            conversations_manager=conv_manager,
            token_limit=4096,
            session=session,
            messages=messages,
            model="gpt-3.5-turbo",
            printer=printer,
        )

        return chat_manager

    def test_exceeding_token_limit_negative(self):
        """Tests exceeding_token_limit function."""

        chat_manager = self.set_test()

        self.assertFalse(chat_manager.exceeding_token_limit())

    def test_exceeding_token_limit_positive(self):
        """Tests exceeding_token_limit function."""

        chat_manager = self.set_test()
        chat_manager.total_usage = chat_manager.num_tokens_from_messages()
        chat_manager.token_limit = 5

        self.assertTrue(chat_manager.exceeding_token_limit())

    def test_num_tokens_from_messages(self):
        """Tests num_tokens_from_messages function."""

        chat_manager = self.set_test()
        self.assertEqual(chat_manager.num_tokens_from_messages(), 34)

    def test_num_tokens_from_messages_name(self):
        """Tests num_tokens_from_messages function."""

        chat_manager = self.set_test()
        chat_manager.messages = [
            {"role": "assistant", "name": "Alice", "content": "Hi, I'm Alice."},
            {"role": "user", "content": "Hello Alice!"},
            {
                "role": "assistant",
                "name": "Alice",
                "content": "How can I help you today?",
            },
        ]

        expected_num_tokens = 29
        actual_num_tokens = chat_manager.num_tokens_from_messages()
        assert actual_num_tokens == expected_num_tokens

    def test_reduce_tokens_enough_tokens_to_reduce(self):
        """Tests reduce_tokens function."""
        chat_manager = self.set_test()
        chat_manager.token_limit = 20
        chat_manager.messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi, how can I help you today?"},
            {"role": "user", "content": "What's the weather like?"},
        ]

        chat_manager.reduce_tokens()
        assert chat_manager.total_usage <= chat_manager.token_limit

    def test_reduce_tokens_not_enough_tokens_to_reduce(self):
        """Tests reduce_tokens function."""
        chat_manager = self.set_test()
        chat_manager.token_limit = 25
        chat_manager.messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi, how can I help you today?"},
            {"role": "user", "content": "What's the weather like?"},
            {"role": "assistant", "content": "It's sunny today!"},
            {"role": "user", "content": "Thanks!"},
            {"role": "assistant", "content": "You're welcome!"},
            {"role": "user", "content": "Bye!"},
        ]

        chat_manager.reduce_tokens()
        self.assertGreaterEqual(chat_manager.token_limit, chat_manager.total_usage)

    def test_reduce_tokens_not_enough_tokens_to_reduce_2(self):
        """Tests reduce_tokens function."""
        chat_manager = self.set_test()
        chat_manager.token_limit = 25
        chat_manager.messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi, how can I help you today?"},
            {"role": "user", "content": "What's the weather like?"},
            {"role": "assistant", "content": "It's sunny today!"},
            {"role": "user", "content": "Thanks!"},
            {"role": "assistant", "content": "You're welcome!"},
            {"role": "user", "content": "Bye!"},
        ]

        chat_manager.__total_usage = chat_manager.num_tokens_from_messages()
        self.assertGreaterEqual(chat_manager.token_limit, chat_manager.total_usage)

    def test_reduce_tokens_token_limit_greater_or_equal(self):
        """Tests reduce_tokens function."""

        chat_manager = self.set_test()
        chat_manager.messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi, how can I help you today?"},
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi, how can I help you today?"},
            {"role": "user", "content": "Hello"},
        ]
        chat_manager.token_limit = 20

        chat_manager.total_usage = chat_manager.num_tokens_from_messages()
        reduced = chat_manager.reduce_tokens()

        self.assertEqual(chat_manager.total_usage, 20)
        self.assertEqual(24, reduced)


if __name__ == "__main__":
    unittest.main()
