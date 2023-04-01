"""Print utilities."""
import random
import time

from colorama import Fore, Style
from rich.console import Console
from rich.markdown import Markdown

from terminalgpt import config

CONSOLE = Console()
PRINT_DELAY = 0.007

INSTALL_WELCOME_MESSAGE = (
    Style.BRIGHT
    + Fore.LIGHTBLUE_EX
    + "\n*~ Welcome to TerminalGPT installation wizard ~*\n"
    + Style.RESET_ALL
    + Style.DIM
    + """
Please note that you need to have an OpenAI account to use TerminalGPT and an API key to use TerminalGPT.
If you don't have an OpenAI account, please create one at https://beta.openai.com/signup.
If you don't have an API key, please create one at https://beta.openai.com/account/api-keys.
"""
    + Style.RESET_ALL
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
Great news! You're all set up to use the OpenAI API key. Your files have been saved at {config.BASE_PATH}.
To start chatting with me, just type '{config.APP_NAME}' into your terminal and let the fun begin!

Thanks for choosing TerminalGPT - the coolest personal assistant on the block.
Let's get our programming on!
"""
    + Style.RESET_ALL
)

INSTALL_SMALL_PRINTS = (
    Style.DIM
    + """
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

STOPPED_MESSAGES = [
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


def split_highlighted_string(string):
    """Split a string into blocks of highlighted syntax text and normal text."""

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


def print_slowly(text, delay=PRINT_DELAY):
    """Prints text slowly."""

    try:
        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
    except KeyboardInterrupt:
        print()
    finally:
        print()


def print_markdown_slowly(text: str, style="yellow"):
    """Prints markdown text slowly."""

    text_markdown = ""
    txt_arr = split_highlighted_string(text)

    for txt in txt_arr:
        with CONSOLE.capture() as capture:
            text_markdown = Markdown(txt)
            CONSOLE.print(text_markdown, style=style)
        text_markdown = capture.get()

        if txt.startswith("```"):
            delay = PRINT_DELAY / 10
        else:
            delay = PRINT_DELAY
        print_slowly(text_markdown, delay)


# pylint: disable=W0102
def choose_random_message(messages: list = STOPPED_MESSAGES):
    """Choose a random message from a list of messages."""

    return messages[random.randint(0, len(messages) - 1)]
