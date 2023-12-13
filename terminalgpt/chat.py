import os
import sys
import time

import openai
import tiktoken
from colorama import Back, Fore, Style
from openai import OpenAI
from prompt_toolkit import PromptSession
from tiktoken.core import Encoding
from yaspin import yaspin
from yaspin.spinners import Spinners

from terminalgpt import config
from terminalgpt.conversations import ConversationManager
from terminalgpt.printer import Printer, PrintUtils


class ChatManager:
    def __init__(self, **kwargs):
        self.__tiktoken_encoder: Encoding = tiktoken.get_encoding(config.ENCODING_MODEL)
        self.__convers_manager: ConversationManager = kwargs["conversations_manager"]
        self.__session: PromptSession = kwargs["session"]
        self.__messages: list = kwargs["messages"]
        self.__model = kwargs["model"]
        self.__printer: Printer = kwargs["printer"]
        self.__token_limit: int = kwargs["token_limit"]
        self.__client: OpenAI = kwargs.get("client", None)
        self.__total_usage = 0

    @property
    def messages(self) -> list:
        return self.__messages

    @messages.setter
    def messages(self, messages: list):
        self.__messages = messages

    @property
    def token_limit(self) -> int:
        return self.__token_limit

    @token_limit.setter
    def token_limit(self, token_limit: int):
        self.__token_limit = token_limit

    @property
    def total_usage(self) -> int:
        return self.__total_usage

    @total_usage.setter
    def total_usage(self, total_usage: int):
        self.__total_usage = total_usage

    @property
    def client(self):
        return self.__client

    @client.setter
    def client(self, client: OpenAI):
        self.__client = client

    def __print_usage(self):
        """Prints the total usage"""
        print(
            Fore.LIGHTBLUE_EX
            + f"\nAPI Total Usage: {str(self.__total_usage)} tokens"
            + Style.RESET_ALL
        )
        print(
            Fore.LIGHTCYAN_EX
            + f"Counter Total Usage: {str(self.num_tokens_from_messages())} tokens"
            + Style.RESET_ALL
        )

    def chat_loop(self):
        """Main chat loop."""

        while True:
            # flush stdin
            sys.stdin.flush()

            # Get user input
            user_input = self.__session.prompt()
            self.__printer.printt()

            # Append to messages and send to ChatGPT
            self.__messages.append({"role": "user", "content": user_input})
            self.__total_usage = self.num_tokens_from_messages()

            # Prevent reaching tokens limit
            if self.exceeding_token_limit():
                self.reduce_tokens()

            # Get answer
            try:
                answer = self.get_user_answer(self.__messages)
            except KeyboardInterrupt:
                self.__printer.print_assistant_message(
                    PrintUtils.choose_random_message(
                        PrintUtils.STOPPED_CONTINUE_MESSAGES
                    )
                )
                continue
            except Exception as error:
                self.__printer.print_assistant_message(
                    str(error), color=Back.RED + Style.BRIGHT
                )
                continue

            # Parse total_usage and message from answer
            self.__total_usage = answer.usage.total_tokens

            message = answer.choices[0].message.content

            # Append to messages list for next iteration keeping context
            self.__messages.append({"role": "assistant", "content": message})

            # Save context or wait for some context
            self.__convers_manager.save_context(
                self.__messages, self.__total_usage, self.__token_limit
            )

            # Print answer message
            self.__printer.print_assistant_message(message)

            # Print usage
            if os.environ.get("LOG_LEVEL") == "DEBUG":
                self.__print_usage()

            if user_input == "exit":
                sys.exit()

    def get_user_answer(self, messages: list):
        """Returns the answer from OpenAI API."""
        while True:
            try:
                with yaspin(
                    Spinners.earth,
                    text=Style.BRIGHT + "Assistant:" + Style.RESET_ALL,
                    color="blue",
                    side="right",
                ):
                    return self.__client.chat.completions.create(
                        model=self.__model, messages=messages
                    )
            except openai.RateLimitError:
                self.__messages.pop(1)
                time.sleep(0.5)

    def exceeding_token_limit(self):
        """Returns True if the total_usage is greater than the token limit with some safe buffer."""
        return self.__total_usage > self.__token_limit

    def reduce_tokens(self) -> int:
        """Reduce tokens in messages context."""
        total_reduced_amount = self.__total_usage - self.__token_limit
        reduce_amount = self.__total_usage - self.__token_limit
        tokenized_message = []

        while self.exceeding_token_limit():
            message = self.__messages.pop(1)
            tokenized_message = self.__tiktoken_encoder.encode(message["content"])
            while reduce_amount > 0 and len(tokenized_message) > 0:
                self.__total_usage -= 1
                reduce_amount -= 1
                tokenized_message.pop(0)
            if len(tokenized_message) == 0 and self.exceeding_token_limit():
                reduce_amount -= 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                self.__total_usage -= 4
                for key, _ in message.items():
                    if key == "name":  # if there's a name, the role is omitted
                        reduce_amount += 1  # role is always required and always 1 token
                        self.__total_usage += 1
        if len(tokenized_message) > 0:
            message["content"] = self.__tiktoken_encoder.decode(tokenized_message)
            self.__messages.insert(1, message)
        if os.environ.get("LOG_LEVEL") == "DEBUG":
            self.__print_usage()

        return total_reduced_amount

    def num_tokens_from_messages(self) -> int:
        """Returns the number of tokens used by a list of messages."""
        encoding = tiktoken.get_encoding(config.ENCODING_MODEL)
        num_tokens = 0
        for message in self.__messages:
            num_tokens += (
                4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            )
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens -= 1  # role is always required and always 1 token
        num_tokens -= 2  # every reply is primed with <im_start>assistant
        return num_tokens

    def welcome_message(self, messages: list):
        """Prints the welcome message."""
        print()
        try:
            welcome_message = self.get_user_answer(messages)
            self.__printer.print_assistant_message(
                welcome_message.choices[0].message.content
            )
        except KeyboardInterrupt:
            self.__printer.print_assistant_message(
                PrintUtils.choose_random_message(PrintUtils.STOPPED_MESSAGES),
                color=Fore.YELLOW + Style.RESET_ALL,
            )
            sys.exit(0)
        except Exception as error:
            self.__printer.print_assistant_message(
                str(error), color=Back.RED + Style.BRIGHT
            )
            sys.exit(1)
