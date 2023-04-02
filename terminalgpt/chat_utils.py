""""Chat utils module for terminalgpt."""

import os
import sys
import time

import openai
import tiktoken
from colorama import Back, Fore, Style
from prompt_toolkit import PromptSession
from yaspin import yaspin
from yaspin.spinners import Spinners

from terminalgpt import config, conversations, print_utils

TIKTOKEN_ENCODER = tiktoken.get_encoding(config.ENCODING_MODEL)


def chat_loop(
    conversation_name: str = None,
    **kwargs,
):
    """Main chat loop."""
    token_limit: int = kwargs["token_limit"]
    session: PromptSession = kwargs["session"]
    messages: list = kwargs["messages"]

    while True:
        # Get user input

        # user_input = click.edit() # can edit at vim
        user_input = session.prompt()
        print()

        # Append to messages and send to ChatGPT
        messages.append({"role": "user", "content": user_input})
        total_usage = num_tokens_from_messages(messages)

        # Prevent reaching tokens limit
        if exceeding_token_limit(total_usage, token_limit):
            messages, total_usage = reduce_tokens(
                messages=messages,
                total_usage=total_usage,
                token_limit=token_limit,
            )

        # Get answer
        try:
            answer = get_user_answer(messages)
        except KeyboardInterrupt:
            print(Style.BRIGHT + "Assistant:" + Style.RESET_ALL)
            stopped_message = print_utils.choose_random_message()
            print_utils.print_markdown_slowly(stopped_message)
            continue

        # Parse total_usage and message from answer
        total_usage = answer["usage"]["total_tokens"]
        message = answer["choices"][0]["message"]["content"]

        # Append to messages list for next iteration keeping context
        messages.append({"role": "assistant", "content": message})

        # Save context wait for some context
        if not conversation_name and total_usage > token_limit / 10:
            conversation_name = conversations.create_conversation_name(messages)
        elif conversation_name:
            conversations.save_conversation(messages, conversation_name)

        # Print answer message
        print(Style.BRIGHT + "Assistant:" + Style.RESET_ALL)
        print_utils.print_markdown_slowly(message)

        # Print usage
        if os.environ.get("LOG_LEVEL") == "DEBUG":
            print(
                Fore.LIGHTBLUE_EX
                + f"\nAPI Total Usage: {str(total_usage)} tokens"
                + Style.RESET_ALL
            )
            print(
                Fore.LIGHTCYAN_EX
                + f"Counter Total Usage: {str(num_tokens_from_messages(messages))} tokens"
                + Style.RESET_ALL
            )

        if user_input == "exit":
            sys.exit()


def get_user_answer(messages):
    """Returns the answer from OpenAI API."""

    while True:
        try:
            with yaspin(
                Spinners.earth,
                text=Style.BRIGHT + "Assistant:" + Style.RESET_ALL,
                color="blue",
                side="right",
            ):
                answer = openai.ChatCompletion.create(
                    model=config.MODEL, messages=messages
                )
                return answer
        except openai.error.RateLimitError as error:
            print_utils.print_slowly(
                Back.RED + Style.BRIGHT + str(error) + Style.RESET_ALL
            )
            waiting_before_trying_again()
        except openai.error.InvalidRequestError as error:
            if "Please reduce the length of the messages" in str(error):
                messages.pop(1)
            else:
                raise error


def exceeding_token_limit(total_usage: int, token_limit: int):
    """Returns True if the total_usage is greater than the token limit with some safe buffer."""

    return total_usage > token_limit


def reduce_tokens(messages: list, token_limit: int, total_usage: int):
    """Reduce tokens in messages context."""

    reduce_amount = total_usage - token_limit
    while exceeding_token_limit(total_usage, token_limit):
        message = messages.pop(1)
        tokenized_message = TIKTOKEN_ENCODER.encode(message["content"])

        while reduce_amount > 0 and len(tokenized_message) > 0:
            total_usage -= 1
            reduce_amount -= 1
            tokenized_message.pop(0)

        if len(tokenized_message) == 0 and exceeding_token_limit(
            total_usage, token_limit
        ):
            # every message follows <im_start>{role/name}\n{content}<im_end>\n
            # thus we need to remove 4 tokens for every message that will be removed
            # so if the message is empty
            reduce_amount -= 4
            total_usage -= 4

            for key, _ in message.items():
                if key == "name":  # if there's a name, the role is omitted
                    # role is always required and always 1 token
                    reduce_amount += 1
                    total_usage += 1

    if len(tokenized_message) > 0:
        message["content"] = TIKTOKEN_ENCODER.decode(tokenized_message)
        messages.insert(1, message)

    if os.environ.get("LOG_LEVEL") == "DEBUG":
        counted_tokens = num_tokens_from_messages(messages)
        print(f"Counted usage: {total_usage}")
        print(f"Real usage tokens: {counted_tokens}")

    return messages, total_usage


def num_tokens_from_messages(messages) -> int:
    """Returns the number of tokens used by a list of messages."""

    encoding = tiktoken.get_encoding(config.ENCODING_MODEL)
    num_tokens = 0
    for message in messages:
        num_tokens += (
            4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        )
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens -= 2  # every reply is primed with <im_start>assistant
    return num_tokens


def waiting_before_trying_again(wait_time: int = 10):
    """Waits for a given time before trying again."""

    with yaspin() as spinner:
        for i in range(wait_time):
            spinner.text = (
                Style.BRIGHT + f"Trying again in {wait_time - i}" + Style.RESET_ALL
            )
            spinner.color = "red"
            time.sleep(1)


# pylint: disable=W0102, W0621
def welcome_message(messages: list):
    """Prints the welcome message."""

    print()
    welcome_message = get_user_answer(messages)
    print(Style.BRIGHT + "\nAssistant:" + Style.RESET_ALL)
    print_utils.print_markdown_slowly(
        welcome_message["choices"][0]["message"]["content"]
    )
