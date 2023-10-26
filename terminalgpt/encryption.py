"""Encryption module for terminalgpt."""

import os
import sys

import openai
from colorama import Fore, Style
from cryptography.fernet import Fernet

from terminalgpt import config


class EncryptionManager:
    """Manages encryption and decryption of secrets."""

    def __init__(self):
        self.__key_path = config.KEY_PATH

    def set_encryption_key(self):
        """Sets the encryption key for OpenAI API."""

        key = Fernet.generate_key()

        try:
            if not os.path.exists(os.path.dirname(self.__key_path)):
                os.makedirs(os.path.dirname(self.__key_path))

            with open(self.__key_path, "wb") as file:
                file.write(key)
        except OSError:
            print(
                Style.BRIGHT
                + Fore.RED
                + f"""
                Failed to create encryption key at {self.__key_path}.
                Please check your permissions and try again.
                """
                + Style.RESET_ALL
            )
            sys.exit(1)

        return key

    def get_encryption_key(self):
        """Generates a key and save it into a file"""

        key = ""

        try:
            with open(self.__key_path, "rb") as file:
                key = file.read()
        except OSError:
            print(
                Style.BRIGHT
                + Fore.RED
                + f"""
                Failed to read encryption key from {self.__key_path}.
                Please check your permissions and try again.
                """
                + Style.RESET_ALL
            )
            sys.exit(1)

        return key

    def encrypt(self, secret: bytes, key):
        """Encrypts a secret using Fernet encryption."""

        # Create a Fernet cipher using the key
        cipher = Fernet(key)

        # Encrypt the secret
        return cipher.encrypt(secret)

    def decrypt(self, file_path, key):
        """Decrypts a secret using Fernet encryption."""

        # Read the encrypted secret from the file
        with open(file_path, "rb") as file:
            encrypted_secret = file.read()

        # Create a Fernet cipher using the key
        cipher = Fernet(key)

        # Decrypt the secret
        return cipher.decrypt(encrypted_secret).decode()

    def check_api_key(self):
        """Checks if the API key is installed."""

        message = f"""
        OpenAI API key is missing!
        Please install OpenAI API key first with '{config.APP_NAME} install' command.
        """

        if (
            not os.path.exists(config.SECRET_PATH)
            and "OPENAI_API_KEY" not in os.environ
        ):
            print(Style.BRIGHT + Fore.RED + message + Style.RESET_ALL)
            sys.exit(1)

    def set_api_key(self):
        """Sets the API key for OpenAI API."""
        if os.environ.get("OPENAI_API_KEY"):
            openai.api_key = os.environ.get("OPENAI_API_KEY")
        else:
            self.check_api_key()
            key = self.get_encryption_key()
            openai.api_key = self.decrypt(config.SECRET_PATH, key)
