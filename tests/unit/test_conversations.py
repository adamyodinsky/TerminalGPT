import unittest
import os
import json
from unittest.mock import MagicMock, patch
from terminalgpt import conversations, config


class TestConversations(unittest.TestCase):
    def setUp(self):
        self.test_conversation_path = "test_conversations"
        config.CONVERSATIONS_PATH = self.test_conversation_path

    def tearDown(self):
        if os.path.exists(self.test_conversation_path):
            for filename in os.listdir(self.test_conversation_path):
                os.remove(os.path.join(self.test_conversation_path, filename))
            os.rmdir(self.test_conversation_path)

    def test_create_conversation_name_empty_messages(self):
        messages = []

        with patch(
            "terminalgpt.conversations.get_system_answer"
        ) as mock_get_system_answer:
            mock_get_system_answer.return_value = {
                "choices": [{"message": {"content": "Test conversation name"}}]
            }
            result = conversations.create_conversation_name(messages)
            self.assertEqual(result, "Test conversation name")

    def test_save_conversation_empty_messages(self):
        messages = []
        file_name = "test_conversation_empty.json"

        conversations.save_conversation(
            messages, file_name, self.test_conversation_path
        )
        self.assertTrue(
            os.path.exists(os.path.join(self.test_conversation_path, file_name))
        )

    def test_load_conversation_non_existent(self):
        messages = conversations.load_conversation(
            "non_existent_file.json", self.test_conversation_path
        )
        self.assertEqual(messages, [])

    def test_is_conversations_empty_non_empty(self):
        message = "No conversations found."
        self.assertFalse(
            conversations.is_conversations_empty(["test_conversation.json"], message)
        )

    def test_create_conversation_name(self):
        messages = [{"role": "user", "content": "Test message"}]

        with patch(
            "terminalgpt.conversations.get_system_answer"
        ) as mock_get_system_answer:
            mock_get_system_answer.return_value = {
                "choices": [{"message": {"content": "Test conversation name"}}]
            }
            result = conversations.create_conversation_name(messages)
            self.assertEqual(result, "Test conversation name")

    def test_save_conversation(self):
        messages = [{"role": "user", "content": "Test message"}]
        file_name = "test_conversation.json"

        conversations.save_conversation(
            messages, file_name, self.test_conversation_path
        )
        self.assertTrue(
            os.path.exists(os.path.join(self.test_conversation_path, file_name))
        )

    def test_delete_conversation(self):
        if not os.path.exists(self.test_conversation_path):
            os.makedirs(self.test_conversation_path)

        file_name = "test_conversation.json"
        file_path = os.path.join(self.test_conversation_path, file_name)
        with open(file_path, "w") as f:
            json.dump([{"role": "user", "content": "Test message"}], f)

        conversations.delete_conversation(file_name, self.test_conversation_path)
        self.assertFalse(os.path.exists(file_path))

    def test_load_conversation(self):
        if not os.path.exists(self.test_conversation_path):
            os.makedirs(self.test_conversation_path)

        messages = [{"role": "user", "content": "Test message"}]
        file_name = "test_conversation.json"

        with open(os.path.join(self.test_conversation_path, file_name), "w") as f:
            json.dump(messages, f)

        loaded_messages = conversations.load_conversation(
            file_name, self.test_conversation_path
        )
        self.assertEqual(loaded_messages, messages)

    def test_get_conversations(self):
        if not os.path.exists(self.test_conversation_path):
            os.makedirs(self.test_conversation_path)

        file_name = "test_conversation.json"
        with open(os.path.join(self.test_conversation_path, file_name), "w") as f:
            pass

        result = conversations.get_conversations(self.test_conversation_path)
        self.assertTrue(file_name in result)

    def test_get_system_answer(self):
        messages = [{"role": "user", "content": "Test message"}]

        with patch("openai.ChatCompletion.create") as mock_openai_create:
            mock_openai_create.return_value = {
                "choices": [{"message": {"content": "Test response"}}]
            }
            result = conversations.get_system_answer(messages)
            self.assertEqual(
                result["choices"][0]["message"]["content"], "Test response"
            )

    def test_is_conversations_empty(self):
        message = "No conversations found."
        self.assertTrue(conversations.is_conversations_empty([], message))


if __name__ == "__main__":
    unittest.main()
