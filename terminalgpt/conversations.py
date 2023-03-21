"""Conversations module."""

import json
import os
import time

import openai
from colorama import Back, Style

from terminalgpt import config, print_utils


def create_conversation_name(messages: list):
    """Creates a context file name based on the title of the conversation."""

    files = get_conversations()

    message_suffix = f"- Keep it unique amongst the next file names list: {files}"
    title_message = {"role": "system", "content": config.TITLE_MESSAGE + message_suffix}

    answer = get_system_answer(messages + [title_message])
    context_file_name = answer["choices"][0]["message"]["content"]

    return context_file_name


def save_conversation(
    messages: list, file_name: str, path: str = config.CONVERSATIONS_PATH
):
    """Saves a conversation to a file."""

    with open(file=f"{path}/{file_name}", mode="w", encoding="utf-8") as conv_file:
        json.dump(messages, conv_file)


def delete_conversation(conversation, path: str = config.CONVERSATIONS_PATH):
    """Deletes a conversation from a file."""

    os.remove(f"{path}/{conversation}")


def load_conversation(file_name: str, path=config.CONVERSATIONS_PATH) -> list:
    """Loads a conversation from a file. returns a list of messages."""

    try:
        with open(file=f"{path}/{file_name}", mode="r", encoding="utf-8") as conv_file:
            messages = json.load(conv_file)
    except FileNotFoundError:
        error_message = f"Failed loading conversation {file_name} from {path}."
        print_utils.print_slowly(
            Back.RED + Style.BRIGHT + error_message + Style.RESET_ALL
        )

    return messages


def get_conversations(path=config.CONVERSATIONS_PATH):
    """Lists all saved conversations."""

    if not os.path.exists(path):
        os.makedirs(path)

    files = os.listdir(path)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)), reverse=True)

    return files


def get_system_answer(messages):
    """Returns the answer from OpenAI API."""

    while True:
        try:
            answer = openai.ChatCompletion.create(model=config.MODEL, messages=messages)
            return answer
        except openai.error.RateLimitError:
            time.sleep(10)


def is_conversations_empty(files: list, message: str):
    """Checks if the conversations directory is empty."""

    if files == []:
        print_utils.print_slowly(message + Style.RESET_ALL)
        return True
    return False
