import getpass
import os

import click
from colorama import Style, Fore
import openai
from terminalgpt import chat_utils
from terminalgpt import config
from terminalgpt import encryption
from terminalgpt import conversations as conv
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style as PromptStyle
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt


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
    help="Creating a secret api key for the chatbot. You will be asked to enter your OpenAI API key."
)
def install():
    # Get API key from user
    chat_utils.print_slowly(config.INSTALL_WELCOME_MESSAGE, 0.005)
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

    chat_utils.print_slowly(config.INSTALL_SUCCESS_MESSAGE, 0.005)
    chat_utils.print_slowly(config.INSTALL_ART, 0.002)
    chat_utils.print_slowly(config.INSTALL_SMALL_PRINTS, 0.007)


@cli.command(help="Start a new conversation.")
@click.pass_context
def new(ctx):
    messages = [
        config.INIT_SYSTEM_MESSAGE,
    ]

    chat_utils.welcome_message(messages)

    chat_utils.chat_loop(
        debug=ctx.obj["DEBUG"],
        token_limit=ctx.obj["TOKEN_LIMIT"],
        session=ctx.obj["SESSION"],
        messages=messages,
    )


@cli.command(help="Choose a previous conversation to load.")
@click.pass_context
def load(ctx):
    # get conversations list
    conversations_list = conv.get_conversations()
    completer = WordCompleter(conversations_list)
    chat_utils.print_slowly(config.CONVERSATIONS_INIT_MESSAGE)

    # print conversations list
    for conversation in conversations_list:
        chat_utils.print_slowly(Style.BRIGHT + "- " + conversation)

    # prompt user to choose a conversation and load it into messages
    conversation = prompt(
        "\nChoose a conversation:\n",
        completer=completer,
        style=PromptStyle.from_dict({"prompt": "bold lightblue"}),
    )

    # if conversation not found, return
    if conversation not in conversations_list:
        chat_utils.print_slowly(
            Style.BRIGHT
            + Fore.RED
            + "\n** Conversation not found! **"
            + Style.RESET_ALL
        )
        return

    # load conversation
    messages = conv.load_conversation(conversation)
    chat_utils.print_slowly(
        Style.BRIGHT
        + Fore.LIGHTBLUE_EX
        + "\n** Conversation " + Fore.WHITE + conversation + Fore.LIGHTBLUE_EX + " Loaded! **\n"
        + "- - - - - - - - - - - - - - - - - - - - - - - - -" + Style.RESET_ALL
    )

    chat_utils.welcome_message(
        messages=messages, init_message=config.INIT_WELCOME_BACK_MESSAGE
    )

    chat_utils.chat_loop(
        debug=ctx.obj["DEBUG"],
        token_limit=ctx.obj["TOKEN_LIMIT"],
        session=ctx.obj["SESSION"],
        messages=messages,
        conversation_name=conversation,
    )


@click.command(help="Choose a previous conversation to load.")
def delete():
    # get conversations list
    conversations_list = conv.get_conversations()
    completer = WordCompleter(conversations_list)
    chat_utils.print_slowly(config.CONVERSATIONS_INIT_MESSAGE)

    # print conversations list
    for conversation in conversations_list:
        chat_utils.print_slowly("- " + conversation)

    # prompt user to choose a conversation and delete it
    while True:
        conversation = prompt(
            "\nChoose a conversation to delete:\n",
            completer=completer,
            style=PromptStyle.from_dict({"prompt": "bold"}),
        )
        # delete file conversation
        if conversation in conversations_list:
            conv.delete_conversation(conversation)
            chat_utils.print_slowly(
                Style.BRIGHT
                + Fore.LIGHTBLUE_EX
                + f"\n** Conversation: '{conversation}' deleted! **"
                + Style.RESET_ALL
            )
            conversations_list = conv.get_conversations()
            completer = WordCompleter(conversations_list)
        else:
            chat_utils.print_slowly(
                Style.BRIGHT
                + Fore.RED
                + "\n** Conversation not found! **"
                + Style.RESET_ALL
            )
        
        if conversations_list == []:
            chat_utils.print_slowly(
                Style.BRIGHT
                + Fore.LIGHTBLUE_EX
                + f"\n** No more conversations to delete! **"
                + Style.RESET_ALL
            )
            return


cli.add_command(install)
cli.add_command(new)
cli.add_command(load)
cli.add_command(delete)

if __name__ == "__main__":
    cli()
