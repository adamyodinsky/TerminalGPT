"""Main module for the terminalgpt package."""

import concurrent.futures
import getpass
import os

import click
import openai
from colorama import Fore, Style
from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style as PromptStyle

from terminalgpt import chat_utils, config, print_utils
from terminalgpt import conversations as conv
from terminalgpt import encryption


@click.group()
@click.option(
    "--debug",
    is_flag=True,
    help="Prints amounts of tokens used.",
    type=bool,
    default=False,
)
@click.option(
    "--token-limit",
    help="Set the token limit between 1024 and 4096.",
    type=int,
    default=config.API_TOKEN_LIMIT,
    callback=chat_utils.validate_token_limit,
)
@click.pass_context
def cli(ctx, debug, token_limit):
    """*~ TerminalGPT - Your Personal Terminal Assistant ~*"""

    ctx.ensure_object(dict)

    ctx.obj["DEBUG"] = debug
    ctx.obj["TOKEN_LIMIT"] = token_limit

    ctx.obj["SESSION"] = PromptSession(
        key_bindings=chat_utils.BINDINGS,
        style=PromptStyle.from_dict({"prompt": "bold"}),
        message="\nUser: ",
    )

    encryption.check_api_key()
    key = encryption.get_encryption_key(config.KEY_PATH)
    openai.api_key = encryption.decrypt(config.SECRET_PATH, key)


@click.command(
    help="Creating a secret api key for the chatbot."
    + " You will be asked to enter your OpenAI API key."
)
def install():
    """Install the terminalgpt openai api key and create app directories."""

    # Get API key from user
    print_utils.print_slowly(print_utils.INSTALL_WELCOME_MESSAGE, 0.005)
    api_key = getpass.getpass(
        prompt=Style.BRIGHT
        + Fore.LIGHTBLUE_EX
        + "Please enter your OpenAI API key:\n"
        + Style.RESET_ALL
    )

    encryption_key = encryption.get_encryption_key(config.KEY_PATH)
    # api_key string to bytes
    encrypted_secret = encryption.encrypt(api_key.encode(), encryption_key)

    if not os.path.exists(os.path.dirname(config.SECRET_PATH)):
        os.makedirs(os.path.dirname(config.SECRET_PATH))

    if not os.path.exists(config.CONVERSATIONS_PATH):
        os.mkdir(config.CONVERSATIONS_PATH)

    # Save the encrypted secret to a file
    with open(config.SECRET_PATH, "wb") as file:
        file.write(encrypted_secret)

    print_utils.print_slowly(print_utils.INSTALL_SUCCESS_MESSAGE, 0.005)
    print_utils.print_slowly(print_utils.INSTALL_ART, 0.002)
    print_utils.print_slowly(print_utils.INSTALL_SMALL_PRINTS, 0.007)


@cli.command(help="Start a new conversation.")
@click.pass_context
def new(ctx):
    """Start a new conversation."""

    messages = [
        config.INIT_SYSTEM_MESSAGE,
    ]

    chat_utils.welcome_message(messages)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(
            chat_utils.chat_loop,
            debug=ctx.obj["DEBUG"],
            token_limit=ctx.obj["TOKEN_LIMIT"],
            session=ctx.obj["SESSION"],
            messages=messages,
            executor=executor,
        )

        future.result()


@cli.command(help="Choose a previous conversation to load.")
@click.pass_context
def load(ctx):
    """Load a previous conversation."""

    # get conversations list
    conversations = conv.get_conversations()

    msg = (
        Style.BRIGHT
        + Fore.RED
        + "\n** There are no conversations to load! **"
        + Style.RESET_ALL
    )

    if conv.is_conversations_empty(files=conversations, message=msg):
        return

    # setup file names auto-completion
    completer = WordCompleter(conversations)
    print_utils.print_slowly(print_utils.CONVERSATIONS_INIT_MESSAGE)

    # print conversations list
    for conversation in conversations:
        print_utils.print_slowly(Style.BRIGHT + "- " + conversation)

    # prompt user to choose a conversation and load it into messages
    conversation = prompt(
        "\nChoose a conversation:\n",
        completer=completer,
        style=PromptStyle.from_dict({"prompt": "bold lightblue"}),
    )

    # if conversation not found, return
    if conversation not in conversations:
        print_utils.print_slowly(
            Style.BRIGHT
            + Fore.RED
            + "\n** Conversation not found! **"
            + Style.RESET_ALL
        )
        return

    # load conversation
    messages = conv.load_conversation(conversation)
    print_utils.print_slowly(
        Style.BRIGHT
        + Fore.LIGHTBLUE_EX
        + "\n** Conversation "
        + Fore.WHITE
        + conversation
        + Fore.LIGHTBLUE_EX
        + " Loaded! **\n"
        + "- - - - - - - - - - - - - - - - - - - - - - - - -"
        + Style.RESET_ALL
    )

    messages.append(config.INIT_WELCOME_BACK_MESSAGE)
    total_usage = chat_utils.num_tokens_from_messages(messages)

    if chat_utils.exceeding_token_limit(total_usage, config.API_TOKEN_LIMIT):
        messages, total_usage = chat_utils.reduce_tokens(
            messages=messages,
            total_usage=total_usage,
            token_limit=config.API_TOKEN_LIMIT,
        )

    chat_utils.welcome_message(messages=messages)

    chat_utils.chat_loop(
        debug=ctx.obj["DEBUG"],
        token_limit=ctx.obj["TOKEN_LIMIT"],
        session=ctx.obj["SESSION"],
        messages=messages,
        conversation_name=conversation,
    )


@click.command(help="Choose a previous conversation to load.")
def delete():
    """Delete previous conversations."""

    # get conversations list
    conversations = conv.get_conversations()

    msg = (
        Style.BRIGHT
        + Fore.RED
        + "\n** There are no conversations to delete! **"
        + Style.RESET_ALL
    )

    if conv.is_conversations_empty(files=conversations, message=msg):
        return

    # setup file names auto completion
    completer = WordCompleter(conversations)
    print_utils.print_slowly(print_utils.CONVERSATIONS_INIT_MESSAGE)

    # print conversations list
    for conversation in conversations:
        print_utils.print_slowly("- " + conversation)

    # prompt user to choose a conversation and delete it
    while True:
        conversation = prompt(
            "\nChoose a conversation to delete:\n",
            completer=completer,
            style=PromptStyle.from_dict({"prompt": "bold"}),
        )

        # delete conversation file
        if conversation in conversations:
            conv.delete_conversation(conversation)

            print_utils.print_slowly(
                Style.BRIGHT
                + Fore.LIGHTBLUE_EX
                + "\n** Conversation "
                + Fore.WHITE
                + conversation
                + Fore.LIGHTBLUE_EX
                + " deleted! **"
                + Style.RESET_ALL
            )

            # update conversations list
            conversations = conv.get_conversations()
            completer = WordCompleter(conversations)
        else:
            print_utils.print_slowly(
                Style.BRIGHT
                + Fore.RED
                + "\n** Conversation not found! **"
                + Style.RESET_ALL
            )

        msg = (
            Style.BRIGHT
            + Fore.LIGHTBLUE_EX
            + "\n** No more conversations to delete! **"
            + Style.RESET_ALL
        )
        if conv.is_conversations_empty(files=conversations, message=msg):
            return


cli.add_command(install)
cli.add_command(new)
cli.add_command(load)
cli.add_command(delete)

# pylint: disable=no-value-for-parameter
if __name__ == "__main__":
    cli()
