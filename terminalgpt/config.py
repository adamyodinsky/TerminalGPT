import platform
from os import path
from colorama import Style, Fore

APP_NAME = "terminalgpt"
API_TOKEN_LIMIT = 4096


BASE_PATH = f"~/.{APP_NAME}".replace("~", path.expanduser("~"))
CONVERSATIONS_PATH = f"{BASE_PATH}/conversations"
SECRET_PATH = f"{BASE_PATH}/{APP_NAME}.encrypted"
KEY_PATH = f"{BASE_PATH}/{APP_NAME}.key"

MODEL = "gpt-3.5-turbo"
ENCODING_MODEL = "cl100k_base"

INIT_SYSTEM_MESSAGE = {
    "role": "system",
    "content": f"""
You are a helpful personal assistant called "TerminalGPT" for a programer on a {platform.platform()} machine.
Please note that your answers will be displayed on the terminal.
So keep them short as possible (5 new lines max) and use a suitable format for printing on terminal.
""",
}


INIT_WELCOME_MESSAGE = {
    "role": "user",
    "content": """
Please start with a random and short greeting message starts with 'Welcome to terminalGPT'.
Add a ton of self humor.
Keep it short as possible, one line.
""",
}

INIT_WELCOME_BACK_MESSAGE = {
    "role": "user",
    "content": """
The conversation you remember was a while ago, now we are continuing it.
Please start the conversation with a random and short welcome back message.
- Start with 'Welcome back to terminalGPT'.
- Add a ton of self humor.
- Keep it short as possible, one line.
""",
}

TITLE_MESSAGE = """
Please give this conversation a short title.
I'm going to use this title as a file name for the conversation.
There are going to a lot of files like that under a folder "~/.terminalgpt/conversations"
- Hard limit of 5 words.
- Use underscores instead of spaces.
- Don't mention yourself in it. (e.g. "TerminalGPT conversation")
- Don't use any special characters.
- Don't use any numbers.
- Don't use any capital letters.
- Don't use any spaces.
- Don't use any punctuation.
- Don't use any symbols.
- Don't use any emojis.
- Don't use any accents.
- Don't use word like: "macos", "programmer_assistant", "conversation".
- Don't use any file extensions. (e.g. ".txt" or ".json")
"""

INSTALL_WELCOME_MESSAGE = (
    Style.BRIGHT
    + Fore.LIGHTBLUE_EX
    + "\n*~ Welcome to TerminalGPT installation wizard ~*\n"
    + Style.RESET_ALL
    + Style.DIM
    + """
Please note that you need to have an OpenAI account to use TerminalGPT and an API key to use TerminalGPT.
If you don't have an OpenAI account, please create one at https://beta.openai.com/signup.
If you don't have an API key, please create one at https://beta.openai.com/account/api-keys.
"""
    + Style.BRIGHT
    + Fore.LIGHTBLUE_EX
    + """
Let's install the OpenAI API key, so you can use TerminalGPT.
"""
)

INSTALL_ART = (
    Style.BRIGHT
    + Fore.GREEN
    + """

 _______                  _             _  _____ _____ _______ 
|__   __|                (_)           | |/ ____|  __ \__   __|
   | | ___ _ __ _ __ ___  _ _ __   __ _| | |  __| |__) | | |   
   | |/ _ \ '__| '_ ` _ \| | '_ \ / _` | | | |_ |  ___/  | |   
   | |  __/ |  | | | | | | | | | | (_| | | |__| | |      | |   
   |_|\___|_|  |_| |_| |_|_|_| |_|\__,_|_|\_____|_|      |_|   

"""
    + Style.RESET_ALL
)

INSTALL_SUCCESS_MESSAGE = (
    Style.BRIGHT
    + Fore.GREEN
    + f"""
Great news! You're all set up to use the OpenAI API key. Your files have been saved at {BASE_PATH}.
To start chatting with me, just type '{APP_NAME}' into your terminal and let the fun begin!

Thanks for choosing TerminalGPT - the coolest personal assistant on the block.
Let's get our programming on!
"""
    + Style.RESET_ALL
)

INSTALL_SMALL_PRINTS = (
    Style.DIM
    + f"""
Just a reminder that TerminalGPT is a free and open source project.
So if you ever feel like contributing or checking out the inner workings of the program,
feel free to head on over to https://github.com/adamyodinsky/TerminalGPT
Thanks for being a part of our community!

"""
    + Style.RESET_ALL
)

CONVERSATIONS_INIT_MESSAGE = (
    Style.BRIGHT
    + Fore.LIGHTBLUE_EX
    + """
Welcome back to TerminalGPT!
Here are your previous conversations:
"""
    + Style.RESET_ALL
)
