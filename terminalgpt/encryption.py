import os

from colorama import Fore, Style
from terminalgpt.config import APP_NAME, SECRET_PATH
from cryptography.fernet import Fernet


def get_encryption_key(key_path):
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
    # Create a Fernet cipher using the key
    cipher = Fernet(key)

    # Encrypt the secret
    return cipher.encrypt(secret)


def decrypt(file_path, key):
    # Read the encrypted secret from the file
    with open(file_path, "rb") as file:
        encrypted_secret = file.read()

    # Create a Fernet cipher using the key
    cipher = Fernet(key)

    # Decrypt the secret
    return cipher.decrypt(encrypted_secret).decode()


def check_api_key():
    message = f"""
OpenAI API key is missing!
Please install the chatbot api key first with '{APP_NAME} install' command.
    """

    if not os.path.exists(SECRET_PATH):
        print(Style.BRIGHT + Fore.RED + message + Style.RESET_ALL)
        exit(1)
