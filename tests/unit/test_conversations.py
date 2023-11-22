import json
import os
import unittest
from unittest.mock import MagicMock, patch

from mocks import ChatCompletionMessageMock, ChatCompletionMock, ChoiceMock

from terminalgpt import config
from terminalgpt.conversations import ConversationManager


class TestConversations(unittest.TestCase):
    def setUp(self):
        self.test_conversation_path = "test_conversations"
        self.test_conversation_name = "test_conversation_name"
        config.CONVERSATIONS_PATH = self.test_conversation_path

    def tearDown(self):
        if os.path.exists(self.test_conversation_path):
            for filename in os.listdir(self.test_conversation_path):
                os.remove(os.path.join(self.test_conversation_path, filename))
            os.rmdir(self.test_conversation_path)

    def create_conversation_manager(self):
        cm = ConversationManager(
            conversation_name=self.test_conversation_name,
            printer=MagicMock(),
            __client=MagicMock(),
        )
        cm.__base_path = self.test_conversation_path
        cm.conversation_name = self.test_conversation_name

        return cm

    def test_create_conversation_name_empty_messages(self):
        cm = self.create_conversation_manager()
        messages = []

        with patch(
            "terminalgpt.conversations.ConversationManager.get_system_answer"
        ) as mock_get_system_answer:
            mock_get_system_answer.return_value = ChatCompletionMock(
                choices=[
                    ChoiceMock(
                        message=ChatCompletionMessageMock(
                            content="Test conversation name"
                        )
                    )
                ]
            )

            cm.create_conversation_name(messages)
            self.assertEqual(cm.conversation_name, "Test conversation name")

    def test_save_conversation_empty_messages(self):
        messages = []
        cm = self.create_conversation_manager()

        cm.save_conversation(messages)
        self.assertTrue(
            os.path.exists(
                os.path.join(self.test_conversation_path, cm.conversation_name)
            )
        )

    def test_load_conversation_non_existent(self):
        cm = self.create_conversation_manager()
        cm.conversation_name = "non_existent_file.json"
        messages = cm.load_conversation()
        self.assertEqual(messages, [])

    def test_is_conversations_empty_non_empty(self):
        cm = self.create_conversation_manager()
        message = "No conversations found."
        self.assertFalse(cm.is_conversations_empty(["test_conversation.json"], message))

    def test_create_conversation_name(self):
        messages = [{"role": "user", "content": "Test message"}]

        with patch(
            "terminalgpt.conversations.ConversationManager.get_system_answer"
        ) as mock_get_system_answer:
            cm = self.create_conversation_manager()
            mock_get_system_answer.return_value = ChatCompletionMock(
                choices=[
                    ChoiceMock(
                        message=ChatCompletionMessageMock(
                            content="Test conversation name"
                        )
                    )
                ]
            )
            cm.create_conversation_name(messages)
            self.assertEqual(cm.conversation_name, "Test conversation name")

    def test_save_conversation(self):
        cm = self.create_conversation_manager()
        messages = [{"role": "user", "content": "Test message"}]

        cm.save_conversation(messages)
        self.assertTrue(
            os.path.exists(
                os.path.join(self.test_conversation_path, cm.conversation_name)
            )
        )

    def test_delete_conversation(self):
        cm = self.create_conversation_manager()
        if not os.path.exists(self.test_conversation_path):
            os.makedirs(self.test_conversation_path)

        file_path = os.path.join(self.test_conversation_path, cm.conversation_name)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([{"role": "user", "content": "Test message"}], f)

        cm.delete_conversation(self.test_conversation_name)
        self.assertFalse(os.path.exists(self.test_conversation_name))

    def test_load_conversation(self):
        cm = self.create_conversation_manager()
        if not os.path.exists(self.test_conversation_path):
            os.makedirs(self.test_conversation_path)

        messages = [{"role": "user", "content": "Test message"}]

        with open(
            os.path.join(self.test_conversation_path, cm.conversation_name),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(messages, f)

        loaded_messages = cm.load_conversation()
        self.assertEqual(loaded_messages, messages)

    def test_get_conversations(self):
        cm = self.create_conversation_manager()
        if not os.path.exists(self.test_conversation_path):
            os.makedirs(self.test_conversation_path)

        with open(
            os.path.join(self.test_conversation_path, cm.conversation_name),
            "w",
            encoding="utf-8",
        ):
            pass

        result = cm.get_conversations()
        self.assertTrue(cm.conversation_name in result)

    def test_is_conversations_empty(self):
        cm = self.create_conversation_manager()
        message = "No conversations found."
        self.assertTrue(cm.is_conversations_empty([], message))


if __name__ == "__main__":
    unittest.main()
