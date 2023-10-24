"""Tests for chat_utils.py."""

import unittest
from unittest.mock import patch

import openai

from terminalgpt import chat, config
from terminalgpt.chat import (
    exceeding_token_limit,
    get_user_answer,
    num_tokens_from_messages,
    reduce_tokens,
)


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

        self.assertTrue(exceeding_token_limit(1025, 1024))
        self.assertFalse(exceeding_token_limit(1000, 1023))

    def test_num_tokens_from_messages(self):
        """Tests num_tokens_from_messages function."""

        messages = self.set_test()
        self.assertEqual(num_tokens_from_messages(messages), 34)

    def test_num_tokens_from_messages_name(self):
        """Tests num_tokens_from_messages function."""

        messages = [
            {"role": "assistant", "name": "Alice", "content": "Hi, I'm Alice."},
            {"role": "user", "content": "Hello Alice!"},
            {
                "role": "assistant",
                "name": "Alice",
                "content": "How can I help you today?",
            },
        ]
        expected_num_tokens = 29
        actual_num_tokens = num_tokens_from_messages(messages)
        assert actual_num_tokens == expected_num_tokens

    def test_reduce_tokens_enough_tokens_to_reduce(self):
        """Tests reduce_tokens function."""

        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi, how can I help you today?"},
            {"role": "user", "content": "What's the weather like?"},
        ]
        token_limit = 20
        total_usage = 25

        _, new_total_usage = reduce_tokens(messages, token_limit, total_usage)
        assert new_total_usage <= token_limit

    def test_reduce_tokens_not_enough_tokens_to_reduce(self):
        """Tests reduce_tokens function."""

        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi, how can I help you today?"},
            {"role": "user", "content": "What's the weather like?"},
            {"role": "assistant", "content": "It's sunny today!"},
            {"role": "user", "content": "Thanks!"},
            {"role": "assistant", "content": "You're welcome!"},
            {"role": "user", "content": "Bye!"},
        ]
        token_limit = 25
        total_usage = chat.num_tokens_from_messages(messages)

        _, new_total_usage = reduce_tokens(messages, token_limit, total_usage)
        assert new_total_usage <= token_limit

    def test_reduce_tokens_token_limit_greater_or_equal(self):
        """Tests reduce_tokens function."""

        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi, how can I help you today?"},
        ]
        token_limit = 20
        total_usage = 15

        reduced_messages, new_total_usage = reduce_tokens(
            messages, token_limit, total_usage
        )
        assert new_total_usage == total_usage
        assert reduced_messages == messages

    def test_reduce_tokens_with_name_key(self):
        """Tests reduce_tokens function."""

        messages = [
            {"role": "user", "content": "Hello"},
            {
                "role": "assistant",
                "content": "Hi, how can I help you today?",
                "name": "Assistant",
            },
            {"role": "user", "content": "What's the weather like?"},
        ]
        token_limit = 20
        total_usage = 28

        _, new_total_usage = reduce_tokens(messages, token_limit, total_usage)
        assert new_total_usage <= token_limit


class TestGetUserAnswer(unittest.TestCase):
    """Tests for get_user_answer function."""

    @patch("openai.ChatCompletion.create")
    def test_get_user_answer_success(self, mock_openai_chatcompletion_create):
        """Tests get_user_answer function."""

        messages = [{"role": "user", "content": "Hello"}]
        mock_response = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Hello there!",
                    }
                }
            ],
            "usage": {
                "total_tokens": 10,
            },
        }
        mock_openai_chatcompletion_create.return_value = mock_response

        answer = get_user_answer(messages, config.DEFAULT_MODEL)
        self.assertEqual(answer, mock_response)

    @patch("openai.ChatCompletion.create")
    @patch("time.sleep")
    def test_get_user_answer_invalid_request_error(
        self, mock_time_sleep, mock_openai_chatcompletion_create
    ):
        """Tests get_user_answer function."""

        error_message = "Please reduce the length of the messages"
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "user", "content": "Hello"},
        ]

        mock_openai_chatcompletion_create.side_effect = [
            openai.InvalidRequestError(error_message, None),
            {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "Hello there!",
                        }
                    }
                ],
                "usage": {
                    "total_tokens": 10,
                },
            },
        ]

        _ = get_user_answer(messages, config.DEFAULT_MODEL)
        mock_openai_chatcompletion_create.assert_called_with(
            model=config.DEFAULT_MODEL, messages=messages
        )
        mock_time_sleep.assert_called_with(0.5)


if __name__ == "__main__":
    unittest.main()
