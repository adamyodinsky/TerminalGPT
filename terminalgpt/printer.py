"""This module contains the Printer class, which is responsible for printing messages to the user."""

import random
import time
from abc import ABC, abstractmethod
from typing import List

from colorama import Fore, Style
from rich.console import Console
from rich.markdown import Markdown

from terminalgpt import config


class Printer(ABC):
    PRINT_DELAY = 0.006

    @abstractmethod
    def printt(self, text: str = ""):
        pass

    def print_assistant_message(self, message, color=Fore.YELLOW):
        pass


class PlainPrinter(Printer):
    def printt(self, text: str = ""):
        try:
            for char in text:
                print(char, end="", flush=True)
                time.sleep(self.PRINT_DELAY)
        except KeyboardInterrupt:
            print()
        finally:
            print()

    def print_assistant_message(self, message, color=Fore.YELLOW):
        """Prints the assistant message."""
        print(Style.BRIGHT + "Assistant:" + Style.RESET_ALL)
        self.printt(color + message + Style.RESET_ALL)


class MarkdownPrinter(Printer):
    def __init__(self):
        self.__console = Console()

    def printt(self, text: str = "", style="yellow"):
        text_markdown = ""
        txt_arr = self._split_highlighted_string(text)
        for txt in txt_arr:
            with self.__console.capture() as capture:
                text_markdown = Markdown(txt)
                self.__console.print(text_markdown, style=style)
            text_markdown = capture.get()
            if txt.startswith("```"):
                delay = self.PRINT_DELAY / 10
            else:
                delay = self.PRINT_DELAY
            self._print_with_delay(text_markdown, delay)

    def print_assistant_message(self, message, color=Fore.YELLOW):
        """Prints the assistant message."""
        print(Style.BRIGHT + "Assistant:" + Style.RESET_ALL)
        self.printt(color + message + Style.RESET_ALL)

    def _split_highlighted_string(self, string: str) -> List[str]:
        result = []
        start = 0
        while True:
            start_block = string.find("```", start)
            if start_block == -1:
                result.append(string[start:])
                break
            end_block = string.find("```", start_block + 3)
            if end_block == -1:
                result.append(string[start:])
                break
            result.append(string[start:start_block])
            result.append(string[start_block : end_block + 3])
            start = end_block + 3
        return result

    def _print_with_delay(self, text: str, delay: float):
        try:
            for char in text:
                print(char, end="", flush=True)
                time.sleep(delay)
        except KeyboardInterrupt:
            print()
        finally:
            print()


class PrinterFactory:
    @staticmethod
    def get_printer(style: str) -> Printer:
        if style == "plain":
            return PlainPrinter()
        if style == "markdown":
            return MarkdownPrinter()

        raise ValueError(f"Invalid style: {style}")


class PrintUtils:
    """A bunch of utility messages"""

    INSTALL_WELCOME_MESSAGE = (
        Style.BRIGHT
        + Fore.LIGHTBLUE_EX
        + "\n*~ Welcome to TerminalGPT installation wizard ~*\n"
        + Style.RESET_ALL
        + """
Please note that you need to have an OpenAI account to use TerminalGPT and an API key to use TerminalGPT.
If you don't have an OpenAI account, please create one at https://beta.openai.com/signup.
If you don't have an API key, please create one at https://beta.openai.com/account/api-keys.
"""
        + Style.BRIGHT
        + Fore.LIGHTBLUE_EX
        + """
Let's install the OpenAI API key, so you can use TerminalGPT.
"""
    )
    # pylint: disable=W1401
    INSTALL_ART = (
        Style.BRIGHT
        + Fore.GREEN
        + """
 _______                  _             _  _____ _____ _______ 
|__   __|                (_)           | |/ ____|  __ \__   __|
   | | ___ _ __ _ __ ___  _ _ __   __ _| | |  __| |__) | | |   
   | |/ _ \ '__| '_ ` _ \| | '_ \ / _` | | | |_ |  ___/  | |   
   | |  __/ |  | | | | | | | | | | (_| | | |__| | |      | |   
   |_|\___|_|  |_| |_| |_|_|_| |_|\__,_|_|\_____|_|      |_|   
"""
        + Style.RESET_ALL
    )

    INSTALL_SUCCESS_MESSAGE = (
        Style.BRIGHT
        + Fore.GREEN
        + f"""
Great news! You're all set up to use TerminalGPT!

Your TerminalGPT files are all saved at {config.BASE_PATH}.
To start chatting with me, just type '{config.APP_NAME}' into your terminal and let the fun begin!

Thanks for choosing TerminalGPT - the coolest personal assistant on the block.
Let's get our programming on!"""
        + Style.RESET_ALL
    )

    INSTALL_SMALL_PRINTS = (
        """
Just a reminder that TerminalGPT is a free and open source project.
So if you ever feel like contributing or checking out the inner workings of the program,
feel free to head on over to https://github.com/adamyodinsky/TerminalGPT
Thanks for being a part of our community!

"""
        + Style.RESET_ALL
    )

    CONVERSATIONS_INIT_MESSAGE = (
        Style.BRIGHT
        + Fore.LIGHTBLUE_EX
        + """
Welcome back to TerminalGPT!
Here are your previous conversations:
"""
        + Style.RESET_ALL
    )

    STOPPED_CONTINUE_MESSAGES = [
        "OK, I stopped. Your wish is my command.",
        "Alright, I stopped. I'm at your service.",
        "OK, I'm all ears. Your wish is my command.",
        "Alright, I paused. I'm at your service.",
        "Alright, I'm waiting for the next instruction.",
        "I've hit pause. Your wish is my command.",
        "Sure thing. Ready and waiting for your next move.",
        "Standing by for your command.",
        "I'm all set, waiting for your orders.",
        "I'm here, awaiting your direction.",
    ]

    STOPPED_MESSAGES = [
        "OK, I stopped. Goodbye.",
        "Alright, I stopped. See you later.",
        "Alright, I paused. Goodbye.",
        "Alright, Goodbye.",
        "I've hit pause. See you later.",
        "Sure thing. See you later.",
    ]

    @staticmethod
    def choose_random_message(messages: List[str]):
        """Chooses a random message from a list of messages."""
        return messages[random.randint(0, len(messages) - 1)]
