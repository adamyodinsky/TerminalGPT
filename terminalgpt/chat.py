import os
import sys
import time

import openai
import tiktoken
from colorama import Back, Fore, Style
from prompt_toolkit import PromptSession
from yaspin import yaspin
from yaspin.spinners import Spinners

from terminalgpt import config
from terminalgpt.conversations import ConversationManager
from terminalgpt.printer import Printer, PrintUtils


class ChatManager:
    def __init__(self, conversations_manager: ConversationManager, **kwargs):
        self.tiktoken_encoder = tiktoken.get_encoding(config.ENCODING_MODEL)
        self.convers_manager = conversations_manager
        self.token_limit = kwargs["token_limit"]
        self.session: PromptSession = kwargs["session"]
        self.messages: list = kwargs["messages"]
        self.model = kwargs["model"]
        self.printer: Printer = kwargs["printer"]

    def set_messages(self, messages: list):
        self.messages = messages

    def set_conversation_name(self, conversation_name: str):
        self.convers_manager.conversation_name = conversation_name

    def chat_loop(self):
        """Main chat loop."""

        while True:
            # flush stdin
            sys.stdin.flush()

            # Get user input
            user_input = self.session.prompt()
            print()

            # Append to messages and send to ChatGPT
            self.messages.append({"role": "user", "content": user_input})
            total_usage = self.num_tokens_from_messages()

            # Prevent reaching tokens limit
            if self.exceeding_token_limit(total_usage):
                self.reduce_tokens(total_usage)

            # Get answer
            try:
                answer = self.get_user_answer(self.messages, self.model)
            except KeyboardInterrupt:
                self.printer.print_assistant_message(
                    PrintUtils.choose_random_message(
                        PrintUtils.STOPPED_CONTINUE_MESSAGES
                    )
                )
                continue
            except Exception as error:
                self.printer.print_assistant_message(
                    str(error), color=Back.RED + Style.BRIGHT
                )
                continue

            # Parse total_usage and message from answer
            total_usage = answer["usage"]["total_tokens"]
            message = answer["choices"][0]["message"]["content"]

            # Append to messages list for next iteration keeping context
            self.messages.append({"role": "assistant", "content": message})

            # Save context or wait for some context
            self.convers_manager.save_context(
                self.messages, total_usage, self.token_limit
            )

            # Print answer message
            self.printer.print_assistant_message(message)

            # Print usage
            if os.environ.get("LOG_LEVEL") == "DEBUG":
                self.print_usage(total_usage)

            if user_input == "exit":
                sys.exit()

    def get_user_answer(self, messages: list, model: str):
        """Returns the answer from OpenAI API."""
        while True:
            try:
                with yaspin(
                    Spinners.earth,
                    text=Style.BRIGHT + "Assistant:" + Style.RESET_ALL,
                    color="blue",
                    side="right",
                ):
                    return openai.ChatCompletion.create(model=model, messages=messages)
            except openai.InvalidRequestError as error:
                if "Please reduce the length of the messages" in str(error):
                    self.messages.pop(1)
                    time.sleep(0.5)
                else:
                    raise error

    def exceeding_token_limit(self, total_usage: int):
        """Returns True if the total_usage is greater than the token limit with some safe buffer."""
        return total_usage > self.token_limit

    def reduce_tokens(self, total_usage: int):
        """Reduce tokens in messages context."""
        reduce_amount = total_usage - self.token_limit
        tokenized_message = []
        while self.exceeding_token_limit(total_usage):
            message = self.messages.pop(1)
            tokenized_message = self.tiktoken_encoder.encode(message["content"])
            while reduce_amount > 0 and len(tokenized_message) > 0:
                total_usage -= 1
                reduce_amount -= 1
                tokenized_message.pop(0)
            if len(tokenized_message) == 0 and self.exceeding_token_limit(total_usage):
                reduce_amount -= 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                total_usage -= 4
                for key, _ in message.items():
                    if key == "name":  # if there's a name, the role is omitted
                        reduce_amount += 1  # role is always required and always 1 token
                        total_usage += 1
        if len(tokenized_message) > 0:
            message["content"] = self.tiktoken_encoder.decode(tokenized_message)
            self.messages.insert(1, message)
        if os.environ.get("LOG_LEVEL") == "DEBUG":
            counted_tokens = self.num_tokens_from_messages()
            print(f"Counted usage: {total_usage}")
            print(f"Real usage tokens: {counted_tokens}")

    def num_tokens_from_messages(self) -> int:
        """Returns the number of tokens used by a list of messages."""
        encoding = tiktoken.get_encoding(config.ENCODING_MODEL)
        num_tokens = 0
        for message in self.messages:
            num_tokens += (
                4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            )
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens -= 1  # role is always required and always 1 token
        num_tokens -= 2  # every reply is primed with <im_start>assistant
        return num_tokens

    def print_usage(self, total_usage):
        """Prints the total usage"""
        print(
            Fore.LIGHTBLUE_EX
            + f"\nAPI Total Usage: {str(total_usage)} tokens"
            + Style.RESET_ALL
        )
        print(
            Fore.LIGHTCYAN_EX
            + f"Counter Total Usage: {str(self.num_tokens_from_messages())} tokens"
            + Style.RESET_ALL
        )

    def welcome_message(self, messages: list):
        """Prints the welcome message."""
        print()
        try:
            welcome_message = self.get_user_answer(messages, config.DEFAULT_MODEL)
            self.printer.print_assistant_message(
                welcome_message["choices"][0]["message"]["content"]
            )
        except KeyboardInterrupt:
            self.printer.print_assistant_message(
                PrintUtils.choose_random_message(PrintUtils.STOPPED_MESSAGES),
                color=Fore.YELLOW + Style.RESET_ALL,
            )
            sys.exit(0)
        except Exception as error:
            self.printer.print_assistant_message(
                str(error), color=Back.RED + Style.BRIGHT
            )
            sys.exit(1)
