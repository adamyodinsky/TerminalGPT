import os
import platform

API_TOKEN_LIMIT = 4096
LOCAL_TOKEN_LIMIT = API_TOKEN_LIMIT / 2

APP_NAME = "terminalgpt"
SECRET_PATH = f"~/.{APP_NAME}/{APP_NAME}.encrypted".replace(
    "~", os.path.expanduser("~")
)
KEY_PATH = f"~/.{APP_NAME}/{APP_NAME}.key".replace("~", os.path.expanduser("~"))

MODEL = "gpt-3.5-turbo"
ENCODING_MODEL = "gpt2"


INIT_SYSTEM_MESSAGE = {
    "role": "system",
    "content": f"""
You are a helpful personal assistant called "TerminalGPT" for a programer on a {platform.platform()} machine.
Please note that your answers will be displayed on the terminal.
So keep them short as possible (7 new lines max) and use a suitable format for printing on terminal.""",
}

INIT_WELCOME_MESSAGE = {
    "role": "user",
    "content": """
Please start with a random and short greeting message starts with 'Welcome to terminalGPT' and some hint of humor, dad jokes style.
Keep it short as possible, one line.
"""
}
