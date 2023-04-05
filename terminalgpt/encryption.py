"""Encryption module for terminalgpt."""

import os
import sys

from colorama import Fore, Style
from cryptography.fernet import Fernet

from terminalgpt import config


def get_encryption_key(key_path):
    """Generates a key and save it into a file"""

    key = None

    if not os.path.exists(key_path):
        os.makedirs(os.path.dirname(key_path))

        key = Fernet.generate_key()
        with open(key_path, "wb") as file:
            file.write(key)
    else:
        with open(key_path, "rb") as file:
            key = file.read()

    return key


def encrypt(secret: bytes, key):
    """Encrypts a secret using Fernet encryption."""

    # Create a Fernet cipher using the key
    cipher = Fernet(key)

    # Encrypt the secret
    return cipher.encrypt(secret)


def decrypt(file_path, key):
    """Decrypts a secret using Fernet encryption."""

    # Read the encrypted secret from the file
    with open(file_path, "rb") as file:
        encrypted_secret = file.read()

    # Create a Fernet cipher using the key
    cipher = Fernet(key)

    # Decrypt the secret
    return cipher.decrypt(encrypted_secret).decode()


def check_api_key():
    """Checks if the API key is installed."""

    message = f"""
OpenAI API key is missing!
Please install OpenAI API key first with '{config.APP_NAME} install' command.
Or you can set the OPENAI_API_KEY environment variable export OPENAI_API_KEY=<your_api_key>
"""

    if not os.path.exists(config.SECRET_PATH) and "OPENAI_API_KEY" not in os.environ:
        print(Style.BRIGHT + Fore.RED + message + Style.RESET_ALL)
        sys.exit(1)
