"""Tests the chat loop end-to-end."""

import os
import sys
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch

import openai
import pexpect
from colorama import Back, Style
from pexpect import TIMEOUT

from terminalgpt import chat, printer


class TestNewCommandIntegration(unittest.TestCase):
    """Tests for get_user_answer function."""

    @patch("openai.ChatCompletion.create")
    def test_chat_loop_e2e_mock(self, mock_openai_chatcompletion_create):
        """Tests the chat loop end-to-end."""

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

    def test_keyboard_interrupt(self):
        messages = "test_message"

        # Mock get_user_answer to raise KeyboardInterrupt
        get_user_answer_mock = MagicMock(side_effect=KeyboardInterrupt)
        printer.choose_random_message_mock = MagicMock(return_value="Random message.")
        printer.print_markdown_slowly_mock = MagicMock()

        with unittest.mock.patch(
            "terminalgpt.chat_utils.get_user_answer", get_user_answer_mock
        ), unittest.mock.patch(
            "terminalgpt.print_utils.choose_random_message",
            printer.choose_random_message_mock,
        ), unittest.mock.patch(
            "terminalgpt.print_utils.print_markdown_slowly",
            printer.print_markdown_slowly_mock,
        ):
            # Redirect stdout to capture printed output
            captured_output = StringIO()
            sys.stdout = captured_output

            try:
                _ = chat.get_user_answer(messages)
            except KeyboardInterrupt:
                print(Style.BRIGHT + "Assistant:" + Style.RESET_ALL)
                stopped_message = printer.choose_random_message()
                printer.print_markdown_slowly(stopped_message)
                self.assertTrue(printer.choose_random_message_mock.called)
                self.assertTrue(printer.print_markdown_slowly_mock.called)

            # Restore stdout
            sys.stdout = sys.__stdout__

    def test_generic_exception(self):
        messages = "test_message"

        # Mock get_user_answer to raise a generic exception
        get_user_answer_mock = MagicMock(side_effect=Exception("Test exception"))
        printer.print_slowly_mock = MagicMock()

        with unittest.mock.patch(
            "terminalgpt.chat_utils.get_user_answer", get_user_answer_mock
        ), unittest.mock.patch(
            "terminalgpt.print_utils.print_slowly", printer.print_slowly_mock
        ):
            # Redirect stdout to capture printed output
            captured_output = StringIO()
            sys.stdout = captured_output

            try:
                answer = chat.get_user_answer(messages)
            except Exception as error:
                print(Style.BRIGHT + "Assistant:" + Style.RESET_ALL)
                printer.print_slowly(
                    Back.RED + Style.BRIGHT + str(error) + Style.RESET_ALL
                )
                self.assertTrue(printer.print_slowly_mock.called)

            # Restore stdout
            sys.stdout = sys.__stdout__

    def test_api_error(self):
        messages = "test_message"

        # Mock get_user_answer to raise APIError
        get_user_answer_mock = MagicMock(
            side_effect=openai.error.APIError("Test API error")
        )
        printer.print_slowly_mock = MagicMock()

        with unittest.mock.patch(
            "terminalgpt.chat_utils.get_user_answer", get_user_answer_mock
        ), unittest.mock.patch(
            "terminalgpt.print_utils.print_slowly", printer.print_slowly_mock
        ):
            # Redirect stdout to capture printed output
            captured_output = StringIO()
            sys.stdout = captured_output

            try:
                answer = chat.get_user_answer(messages)
            except openai.error.APIError as error:
                print(Style.BRIGHT + "Assistant:" + Style.RESET_ALL)
                printer.print_slowly(
                    Back.RED + Style.BRIGHT + str(error) + Style.RESET_ALL
                )
                self.assertTrue(printer.print_slowly_mock.called)

            # Restore stdout
            sys.stdout = sys.__stdout__

    def test_invalid_request_error(self):
        messages = "test_message"

        # Mock get_user_answer to raise InvalidRequestError
        get_user_answer_mock = MagicMock(
            side_effect=openai.error.InvalidRequestError(
                "Test InvalidRequest error", None
            )
        )
        chat.get_user_answer_mock = MagicMock()

        with unittest.mock.patch(
            "terminalgpt.chat_utils.get_user_answer", get_user_answer_mock
        ), unittest.mock.patch(
            "terminalgpt.chat_utils.get_user_answer", chat.get_user_answer_mock
        ):
            # Redirect stdout to capture printed output
            captured_output = StringIO()
            sys.stdout = captured_output

            try:
                answer = chat.get_user_answer(messages)
            except openai.error.InvalidRequestError as error:
                self.assertTrue(chat.get_user_answer_mock.called)

            # Restore stdout
            sys.stdout = sys.__stdout__

    def test_openai_error(self):
        messages = "test_message"

        # Mock get_user_answer to raise OpenAIError
        get_user_answer_mock = MagicMock(
            side_effect=openai.error.OpenAIError("Test OpenAI error")
        )
        printer.print_slowly_mock = MagicMock()

        with unittest.mock.patch(
            "terminalgpt.chat_utils.get_user_answer", get_user_answer_mock
        ), unittest.mock.patch(
            "terminalgpt.print_utils.print_slowly", printer.print_slowly_mock
        ):
            # Redirect stdout to capture printed output
            captured_output = StringIO()
            sys.stdout = captured_output

            try:
                answer = chat.get_user_answer(messages)
            except openai.error.OpenAIError as error:
                print(Style.BRIGHT + "Assistant:" + Style.RESET_ALL)
                printer.print_slowly(
                    Back.RED + Style.BRIGHT + str(error) + Style.RESET_ALL
                )
                self.assertTrue(printer.print_slowly_mock.called)

            # Restore stdout
            sys.stdout = sys.__stdout__


if __name__ == "__main__":
    unittest.main()
