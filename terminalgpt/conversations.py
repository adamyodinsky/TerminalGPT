"""Conversations module."""

import json
import os
import time

import openai
from colorama import Back, Style

from terminalgpt import config, print_utils
from terminalgpt.print_utils import Printer


class ConversationManager:
    """Manages conversations."""

    def __init__(self, printer: Printer, conversation_name: str = ""):
        self.base_path = config.CONVERSATIONS_PATH
        self.conversation_name = conversation_name
        self.printer = printer

    def create_conversation_name(self, messages: list):
        """Creates a context file name based on the title of the conversation."""

        files = self.get_conversations()

        message_suffix = f"- Keep it unique amongst the next file names list: {files}"
        title_message = {
            "role": "system",
            "content": config.TITLE_MESSAGE + message_suffix,
        }

        answer = self.get_system_answer(messages + [title_message])
        context_file_name = answer["choices"][0]["message"]["content"]

        self.conversation_name = context_file_name

    def save_context(self, messages: list, total_usage: int, token_limit: int):
        # Save context or wait for some context
        if not self.conversation_name and total_usage > token_limit / 10:
            self.create_conversation_name(messages)
        elif self.conversation_name:
            self.save_conversation(messages)

    def save_conversation(self, messages: list):
        """Saves a conversation to a file."""

        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

        with open(
            file=f"{self.base_path}/{self.conversation_name}",
            mode="w",
            encoding="utf-8",
        ) as conv_file:
            json.dump(messages, conv_file)

    def delete_conversation(self, conversation_name: str):
        """Deletes a conversation from a file."""

        os.remove(f"{self.base_path}/{conversation_name}")

    def load_conversation(self) -> list:
        """Loads a conversation from a file. returns a list of messages."""

        messages = []

        try:
            with open(
                file=f"{self.base_path}/{self.conversation_name}",
                mode="r",
                encoding="utf-8",
            ) as conv_file:
                messages = json.load(conv_file)
        except FileNotFoundError as error:
            error_message = f"Failed loading conversation {self.conversation_name} from {self.base_path}.\n{str(error)}"
            self.printer.printt(
                Back.RED + Style.BRIGHT + error_message + Style.RESET_ALL
            )
            messages = []

        return messages

    def get_conversations(self):
        """Lists all saved conversations."""

        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

        files = os.listdir(self.base_path)
        files.sort(
            key=lambda x: os.path.getmtime(os.path.join(self.base_path, x)),
            reverse=True,
        )

        return files

    def get_system_answer(self, messages):
        """Returns the answer from OpenAI API."""

        while True:
            try:
                answer = openai.ChatCompletion.create(
                    model=config.DEFAULT_MODEL, messages=messages
                )
                return answer
            except openai.OpenAIError:
                time.sleep(10)

    def is_conversations_empty(self, files: list, message: str):
        """Checks if the conversations directory is empty."""

        if files == []:
            self.printer.print(message + Style.RESET_ALL)
            return True
        return False
