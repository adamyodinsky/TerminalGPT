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

from terminalgpt.chat import ChatManager
from terminalgpt.conversations import ConversationManager
from terminalgpt.printer import PrinterFactory, PrintUtils


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

        printer = PrinterFactory.get_printer("markdown")
        conv_manager = ConversationManager(printer=printer, __client=MagicMock())

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
            client=MagicMock(),
        )

        return chat_manager, printer, messages

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
            side_effect=openai.APIError(
                message="Test API error", request=MagicMock(), body={}
            )
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
            except openai.APIError as error:
                pm.printt(Back.RED + Style.BRIGHT + str(error) + Style.RESET_ALL)
                self.assertTrue(printt_mock.called)

            # Restore stdout
            sys.stdout = sys.__stdout__

    def test_invalid_request_error(self):
        cm, _, _ = self.set_test()
        messages = ["test_message"]

        # Mock get_user_answer to raise InvalidRequestError
        get_user_answer_mock = MagicMock(
            side_effect=openai.BadRequestError(
                message="Test InvalidRequest error", body={}, response=MagicMock()
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
            except openai.BadRequestError:
                self.assertTrue(get_user_answer_mock.called)

            # Restore stdout
            sys.stdout = sys.__stdout__

    def test_openai_error(self):
        cm, pm, _ = self.set_test()
        messages = ["test_message"]

        # Mock get_user_answer to raise OpenAIError
        get_user_answer_mock = MagicMock(
            side_effect=openai.APIError(
                message="Test API error", request=MagicMock(), body={}
            )
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
            except openai.OpenAIError as error:
                print(Style.BRIGHT + "Assistant:" + Style.RESET_ALL)
                pm.printt(Back.RED + Style.BRIGHT + str(error) + Style.RESET_ALL)
                self.assertTrue(printt_mock.called)

            # Restore stdout
            sys.stdout = sys.__stdout__


if __name__ == "__main__":
    unittest.main()
