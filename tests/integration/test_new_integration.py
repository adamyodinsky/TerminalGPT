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
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style as PromptStyle

from terminalgpt import chat, printer
from terminalgpt.chat import ChatManager
from terminalgpt.conversations import ConversationManager
from terminalgpt.printer import Printer, PrinterFactory, PrintUtils


class TestNewCommandIntegration(unittest.TestCase):
    """Tests for get_user_answer function."""

    def set_test(self):
        """Sets a test."""

        messages = [
            {"role": "system", "content": "Hello user Hello user"},
            {"role": "user", "content": "Hello system Hello system"},
            {"role": "assistant", "content": "Hello user Hello user"},
            {"role": "user", "content": "Hello assistant Hello assistant"},
        ]

        printer = PrinterFactory.get_printer(False)
        conv_manager = ConversationManager(printer)

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

        return chat_manager, printer, messages

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
        cm, pm, msg = self.set_test()

        # Mock get_user_answer to raise KeyboardInterrupt
        get_user_answer_mock = MagicMock(side_effect=KeyboardInterrupt)
        choose_random_message_mock = MagicMock(return_value="Random message.")
        printt = MagicMock()

        with patch(
            "terminalgpt.chat.ChatManager.get_user_answer", get_user_answer_mock
        ), patch(
            "terminalgpt.printer.PrintUtils.choose_random_message",
            choose_random_message_mock,
        ), patch(
            "terminalgpt.printer.MarkdownPrinter.printt",
            printt,
        ):
            # Redirect stdout to capture printed output
            captured_output = StringIO()
            sys.stdout = captured_output

            try:
                _ = cm.get_user_answer(msg)
            except KeyboardInterrupt:
                stopped_message = PrintUtils.choose_random_message(["Random message."])
                pm.printt(stopped_message)
                self.assertTrue(choose_random_message_mock.called)
                self.assertTrue(printt.called)

            # Restore stdout
            sys.stdout = sys.__stdout__

    def test_generic_exception(self):
        messages = ["test_message"]
        cm, pm, _ = self.set_test()

        # Mock get_user_answer to raise a generic exception
        get_user_answer_mock = MagicMock(side_effect=Exception("Test exception"))
        printt = MagicMock()

        with patch(
            "terminalgpt.chat.ChatManager.get_user_answer", get_user_answer_mock
        ), patch("terminalgpt.printer.MarkdownPrinter.printt", printt):
            # Redirect stdout to capture printed output
            captured_output = StringIO()
            sys.stdout = captured_output

            try:
                _ = cm.get_user_answer(messages)
            except Exception as error:
                pm.printt(Back.RED + Style.BRIGHT + str(error) + Style.RESET_ALL)
                self.assertTrue(printt.called)

            # Restore stdout
            sys.stdout = sys.__stdout__

    def test_api_error(self):
        messages = ["test_message"]
        cm, pm, _ = self.set_test()

        # Mock get_user_answer to raise APIError
        get_user_answer_mock = MagicMock(
            side_effect=openai.error.APIError("Test API error")
        )
        printt_mock = MagicMock()

        with patch(
            "terminalgpt.chat.ChatManager.get_user_answer", get_user_answer_mock
        ), patch("terminalgpt.printer.MarkdownPrinter.printt", printt_mock):
            # Redirect stdout to capture printed output
            captured_output = StringIO()
            sys.stdout = captured_output

            try:
                _ = cm.get_user_answer(messages)
            except openai.error.APIError as error:
                pm.printt(Back.RED + Style.BRIGHT + str(error) + Style.RESET_ALL)
                self.assertTrue(printt_mock.called)

            # Restore stdout
            sys.stdout = sys.__stdout__

    def test_invalid_request_error(self):
        cm, _, _ = self.set_test()
        messages = ["test_message"]

        # Mock get_user_answer to raise InvalidRequestError
        get_user_answer_mock = MagicMock(
            side_effect=openai.error.InvalidRequestError(
                "Test InvalidRequest error", None
            )
        )
        get_user_answer_mock = MagicMock()

        with patch(
            "terminalgpt.chat.ChatManager.get_user_answer", get_user_answer_mock
        ):
            # Redirect stdout to capture printed output
            captured_output = StringIO()
            sys.stdout = captured_output

            try:
                _ = cm.get_user_answer(messages)
            except openai.error.InvalidRequestError:
                self.assertTrue(get_user_answer_mock.called)

            # Restore stdout
            sys.stdout = sys.__stdout__

    def test_openai_error(self):
        cm, pm, _ = self.set_test()
        messages = ["test_message"]

        # Mock get_user_answer to raise OpenAIError
        get_user_answer_mock = MagicMock(
            side_effect=openai.error.OpenAIError("Test OpenAI error")
        )
        printt_mock = MagicMock()

        with patch(
            "terminalgpt.chat.ChatManager.get_user_answer", get_user_answer_mock
        ), patch("terminalgpt.printer.MarkdownPrinter.printt", printt_mock):
            # Redirect stdout to capture printed output
            captured_output = StringIO()
            sys.stdout = captured_output

            try:
                _ = cm.get_user_answer(messages)
            except openai.error.OpenAIError as error:
                print(Style.BRIGHT + "Assistant:" + Style.RESET_ALL)
                pm.printt(Back.RED + Style.BRIGHT + str(error) + Style.RESET_ALL)
                self.assertTrue(printt_mock.called)

            # Restore stdout
            sys.stdout = sys.__stdout__


if __name__ == "__main__":
    unittest.main()
