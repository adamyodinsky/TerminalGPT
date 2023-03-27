"""Print utilities."""
import random
import time

from colorama import Fore, Style

from terminalgpt import config

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


def print_slowly(text, delay=0.008):
    """Prints text slowly."""

    try:
        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
    except KeyboardInterrupt:
        print()
    finally:
        print()


# pylint: disable=W0102
def choose_random_message(messages: list = STOPPED_MESSAGES):
    """Choose a random message from a list of messages."""

    return messages[random.randint(0, len(messages) - 1)]
