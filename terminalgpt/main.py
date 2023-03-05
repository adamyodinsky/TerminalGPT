import os
from colorama import Fore, Back, Style
import platform
import tiktoken
import openai
import time

API_TOKEN_LIMIT = 4096
LOCAL_TOKEN_LIMIT = API_TOKEN_LIMIT / 2

MODEL = "gpt-3.5-turbo"
ENCODING_MODEL = "gpt2"

TIKTOKEN_ENCODER = tiktoken.get_encoding(ENCODING_MODEL)


INIT_SYSTEM_MESSAGE = {
    "role": "system",
    "content": f"""
You are a helpful terminal assistant for a programer on a {platform.platform()} machine.
Please note that your answers will be displayed on the terminal.
So keep them short as possible (7 new lines max) and use a suitable format for printing on terminal.""",
}


def main():
    try:
        chat_loop()
    except KeyboardInterrupt:
        print(Style.BRIGHT + Fore.CYAN + "\n\nExiting..." + Style.RESET_ALL)
        exit(0)


def chat_loop():
    total_usage = 0
    messages = [
        INIT_SYSTEM_MESSAGE,
    ]

    while True:
        # Get user input
        user_input = input(Style.BRIGHT + "\nUser: " + Style.RESET_ALL)
        usage = num_tokens_from_string(user_input)

        # Prevent reaching tokens limit
        while total_usage + usage >= LOCAL_TOKEN_LIMIT:
            # When reaching the limit, remove half of the oldest messages from the context
            while total_usage + usage >= LOCAL_TOKEN_LIMIT / 2:
                popped_message = messages.pop(0)
                total_usage -= num_tokens_from_string(popped_message["content"])

            if total_usage + usage < LOCAL_TOKEN_LIMIT:
                messages.insert(0, INIT_SYSTEM_MESSAGE)

        # Append to messages and send to ChatGPT
        messages.append({"role": "user", "content": user_input})

        # Get answer
        answer = get_answer(messages)

        # Parse usage and message from answer
        total_usage = answer["usage"]["total_tokens"]
        message = answer["choices"][0]["message"]["content"]

        # Append to messages list for next iteration keeping context
        messages.append({"role": "assistant", "content": message})

        # Print answer message
        print(Style.BRIGHT + "\nAssistant:" + Style.RESET_ALL)
        print_slowly(Fore.YELLOW + message + Style.RESET_ALL)

        # Print usage
        if os.getenv("DEBUG") == "True":
            print(
                Back.LIGHTBLUE_EX
                + "Total Usage: "
                + str(total_usage)
                + " tokens"
                + Style.RESET_ALL
            )


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    num_tokens = len(TIKTOKEN_ENCODER.encode(string))
    return num_tokens


def get_answer(messages):
    answer = openai.ChatCompletion.create(model=MODEL, messages=messages)
    return answer


def print_slowly(text, delay=0.02):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()
