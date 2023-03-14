import getpass
import os

import click
from colorama import Style, Fore
from terminalgpt.chat_utils import chat_loop, validate_token_limit
from terminalgpt.config import KEY_PATH, SECRET_PATH, API_TOKEN_LIMIT
from terminalgpt.encryption import check_api_key, decrypt, encrypt, get_encryption_key


@click.group()
def cli():
    pass


@click.command(
    help="Creating a secret api key for the chatbot. You will be asked to enter your OpenAI API key."
)
def install():
    # Get API key from user
    api_key = getpass.getpass(
        prompt=Style.BRIGHT + "OpenAI API Key: " + Style.RESET_ALL
    )

    encryption_key = get_encryption_key(KEY_PATH)
    # api_key string to bytes
    encrypted_secret = encrypt(api_key.encode(), encryption_key)

    if not os.path.exists(os.path.dirname(SECRET_PATH)):
        os.makedirs(os.path.dirname(SECRET_PATH))

    # Save the encrypted secret to a file
    with open(SECRET_PATH, "wb") as file:
        file.write(encrypted_secret)

    print(
        Style.BRIGHT
        + Fore.GREEN
        + f"OpenAI API Key Encrypted and saved at {os.path.dirname(SECRET_PATH)}"
        + Style.RESET_ALL
    )


@click.command(
    help="Start the chatbot. You will be asked to enter your OpenAI API key."
)
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
    default=API_TOKEN_LIMIT,
    callback=validate_token_limit,
)
def chat(debug, token_limit):
    check_api_key()
    key = get_encryption_key(KEY_PATH)
    api_key = decrypt(SECRET_PATH, key)
    chat_loop(debug, api_key, token_limit)


cli.add_command(install)
cli.add_command(chat)

if __name__ == "__main__":
    cli()
