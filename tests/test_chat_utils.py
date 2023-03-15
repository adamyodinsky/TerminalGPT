import unittest

from terminalgpt import chat_utils

class TestEncryption(unittest.TestCase):
    def set_test(self):
        messages = [
          {"role": "system", "content": "Hello user"},
          {"role": "user", "content": "Hello system"},
          {"role": "assistant", "content": "Hello user"},
          {"role": "user", "content": "Hello assistant"},
        ]
        return messages

    def test_exceeding_token_limit(self):
        self.assertTrue(chat_utils.exceeding_token_limit(1025, 1024))
        self.assertFalse(chat_utils.exceeding_token_limit(1000, 1023))

    def test_validate_token_limit(self):
        self.assertEqual(chat_utils.validate_token_limit(None, None, 1024), 1024)
        self.assertEqual(chat_utils.validate_token_limit(None, None, 2048), 2048)
        self.assertEqual(chat_utils.validate_token_limit(None, None, 4096), 4096)

        with self.assertRaises(ValueError):
            chat_utils.validate_token_limit(None, None, 8192)

        with self.assertRaises(ValueError):
            chat_utils.validate_token_limit(None, None, 1023)

    def test_count_all_tokens(self):
        messages = self.set_test()
        total_usage = chat_utils.count_all_tokens(messages)
        self.assertEqual(total_usage, 27)

    def test_reduce_tokens(self):
        token_limit = 26
        messages = self.set_test()
        total_usage = chat_utils.count_all_tokens(messages)

        print("total_usage:", total_usage)
        messages, total_usage = chat_utils.reduce_tokens(
            messages, token_limit, total_usage
        )

        self.assertEqual(total_usage, token_limit)
        self.assertEqual(len(messages), 4)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[0]["content"], "Hello user")
        self.assertEqual(messages[1]["role"], "user")
        self.assertEqual(messages[1]["content"], " system")

        token_limit = 21
        messages = self.set_test()
        total_usage = chat_utils.count_all_tokens(messages)

        messages, total_usage = chat_utils.reduce_tokens(
            messages, token_limit, total_usage
        )

        self.assertEqual(total_usage, token_limit)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[0]["content"], "Hello user")
        self.assertEqual(messages[1]["role"], "user")
        self.assertEqual(messages[1]["content"], "")
        


if __name__ == "__main__":
    unittest.main()