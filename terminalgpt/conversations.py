import json
import os

from colorama import Back, Style
from terminalgpt import config
from terminalgpt import chat_utils


def create_conversation_name(messages: list):
    """Creates a context file name based on the title of the conversation."""

    files_list = get_conversations()

    message_suffix = f"- Keep it unique amongst the next file names list: {files_list}"
    title_message = {"role": "user", "content": config.TITLE_MESSAGE + message_suffix}

    answer = chat_utils.get_system_answer(messages + [title_message])
    context_file_name = answer["choices"][0]["message"]["content"]

    return context_file_name


def save_conversation(
    messages: list, file_name: str, path: str = config.CONVERSATIONS_PATH
):
    """Saves a conversation to a file."""

    with open(f"{path}/{file_name}", "w") as f:
        json.dump(messages, f)

def delete_conversation(conversation, path: str = config.CONVERSATIONS_PATH):
    """Deletes a conversation from a file."""

    os.remove(f"{path}/{conversation}")
    
def load_conversation(file_name: str, path=config.CONVERSATIONS_PATH) -> list:
    """Loads a conversation from a file. returns a list of messages."""

    try: 
      with open(f"{path}/{file_name}", "r") as f:
          messages = json.load(f)
    except:        
      error_message = f"Failed loading conversation {file_name} from {path}."
      chat_utils.print_slowly(Back.RED + Style.BRIGHT + error_message + Style.RESET_ALL)

    return messages


def get_conversations(path=config.CONVERSATIONS_PATH):
    """Lists all saved conversations."""

    files = os.listdir(path)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)), reverse=True)

    return files
