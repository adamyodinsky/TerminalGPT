import time

import openai
import tiktoken
from colorama import Back, Fore, Style
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style as PromptStyle
from yaspin import yaspin
from yaspin.spinners import Spinners

from terminalgpt.config import (ENCODING_MODEL, INIT_SYSTEM_MESSAGE,
                                INIT_WELCOME_MESSAGE, MODEL)

TIKTOKEN_ENCODER = tiktoken.get_encoding(ENCODING_MODEL)


# TODO: multiline input with editing capabilities
def chat_loop(debug: bool, api_key: str, token_limit: int):
    """Main chat loop."""

    openai.api_key = api_key
    messages = [
        INIT_SYSTEM_MESSAGE,
    ]

    # Prompt toolkit style
    prompt_style = PromptStyle.from_dict({"prompt": "bold"})
    session = PromptSession(style=prompt_style)

    # Print welcome message
    print()
    welcome_message = get_answer(messages + [INIT_WELCOME_MESSAGE])
    print(Style.BRIGHT + "\nAssistant:" + Style.RESET_ALL)
    print_slowly(
        Fore.YELLOW
        + welcome_message["choices"][0]["message"]["content"]
        + Style.RESET_ALL
    )

    while True:
        # Get user input
        user_input = session.prompt("\nUser: ")
        print()

        # Append to messages and send to ChatGPT
        messages.append({"role": "user", "content": user_input})
        total_usage = count_all_tokens(messages, TIKTOKEN_ENCODER)

        # Prevent reaching tokens limit
        if exceeding_token_limit(total_usage, token_limit):
            messages, total_usage = reduce_tokens(
                messages=messages,
                total_usage=total_usage,
                token_limit=token_limit,
            )

        # Get answer
        answer = get_answer(messages)

        # Parse curr_usage and message from answer
        total_usage = answer["usage"]["total_tokens"]
        message = answer["choices"][0]["message"]["content"]

        # Append to messages list for next iteration keeping context
        messages.append({"role": "assistant", "content": message})

        # Print answer message
        print(Style.BRIGHT + "Assistant:" + Style.RESET_ALL)
        print_slowly(Fore.YELLOW + message + Style.RESET_ALL)

        # Print usage
        if debug:
            print(
                Back.LIGHTBLUE_EX
                + f"\nAPI Total Usage: {str(total_usage)} tokens"
                + Style.RESET_ALL
            )
            print(
                Back.LIGHTCYAN_EX
                + f"\nCounter Total Usage: {str(count_all_tokens(messages, TIKTOKEN_ENCODER))} tokens"
                + Style.RESET_ALL
            )

        if user_input == "exit":
            exit(0)


def get_answer(messages):
    """Returns the answer from OpenAI API."""

    with yaspin(
        Spinners.earth,
        text=Style.BRIGHT + "Assistant:" + Style.RESET_ALL,
        color="blue",
        side="right",
    ):
        answer = openai.ChatCompletion.create(model=MODEL, messages=messages)
        return answer


def print_slowly(text, delay=0.01):
    """Prints text slowly."""

    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def validate_token_limit(ctx, param, limit: int):
    """Validates the token limit."""

    if limit < 1024 and limit > 4096:
        raise ValueError("Token limit must be between 1024 and 4096")
    return limit


def exceeding_token_limit(total_usage: int, token_limit: int):
    """Returns True if the total_usage is greater than the token limit with some safe buffer."""

    return total_usage >= token_limit


def reduce_tokens(messages: list, token_limit: int, total_usage: int):
    """Reduce tokens in messages until exceeding_token_limit is False."""

    while exceeding_token_limit(total_usage, token_limit):
        reduce_amount = total_usage - token_limit + 100
        message = messages.pop(1)
        tokenized_message = TIKTOKEN_ENCODER.encode(message["content"])

        while reduce_amount > 0 and len(tokenized_message) > 0:
            total_usage -= 1
            reduce_amount -= 1
            tokenized_message.pop(0)

    message["content"] = TIKTOKEN_ENCODER.decode(tokenized_message)
    messages.insert(1, message)
    return messages, total_usage


def count_all_tokens(messages, encoder):
    """Returns the total number of tokens in a list of messages."""

    total_tokens = 0
    for message in messages:
        total_tokens += len(encoder.encode("content: " + message["content"]))
        total_tokens += len(encoder.encode("role: " + message["role"]))

    return total_tokens - 1
