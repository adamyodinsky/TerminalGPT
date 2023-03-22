# ![TerminalGPT](logo.png)

[![Continuous Integration](https://github.com/adamyodinsky/TerminalGPT/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/adamyodinsky/TerminalGPT/actions/workflows/main.yml) ![PyPI](https://img.shields.io/pypi/v/terminalgpt) ![PyPI - Downloads](https://img.shields.io/pypi/dm/terminalgpt) ![commits-since](https://img.shields.io/github/commits-since/adamyodinsky/TerminalGPT/latest) ![GitHub last commit](https://img.shields.io/github/last-commit/adamyodinsky/terminalgpt)

Welcome to terminalGPT, the terminal-based ChatGPT personal assistant app!
With terminalGPT, you can easily interact with the OpenAI GPT 3.5 language model.

Whether you need help with a quick question or want to explore a complex topic, TerminalGPT is here to assist you. Simply enter your query and TerminalGPT will provide you with the best answer possible based on its extensive knowledge base.

---

![Alt Text](./usage.gif)

---

## Why?

Some advantages of using TerminalGPT over the chatGPT browser-based app:

1. It doesn't disconnect like the browser-based app, so you can leave it running in a terminal session on the side without losing context.
2. It's highly available and can be used whenever you need it.
3. It's faster with replies than the browser-based app.
4. You can use TerminalGPT with your IDE terminal, which means you won't have to constantly switch between your browser and your IDE when you have questions.
5. TerminalGPT's answers are tailored to your machine's operating system, distribution, and chip-set architecture.
6. Doesn't use your conversation data for training the model (unlike the browser-based app).
7. Your conversations are stored locally on your machine, so only you can access them.

## Pre-requisites

1. Python 3.6 or higher
2. An OpenAI Account and API key (It's free for personal use).
[How to create OpenAI API keys](https://elephas.app/blog/how-to-create-openai-api-keys-cl5c4f21d281431po7k8fgyol0)

## Installation

1. Install the latest TerminalGPT with pip install.

```sh
pip install terminalgpt -U
```

2. Now you have `terminalgpt` command available in your terminal. Run the following install command to configure the app.

```sh
terminalgpt install
```

3. Enter your OpenAI API key when prompted and press enter.

That's it! You're ready to use TerminalGPT!

---

## Usage

```sh
Usage: terminalgpt [OPTIONS] COMMAND [ARGS]...

Options:
  --debug                Prints amounts of tokens used.
  --token-limit INTEGER  Set the token limit between 1024 and 4096.
  --help                 Show this message and exit.

Commands:
  new      Start a new conversation.
  load     Choose a previous conversation to load.
  delete   Choose a previous conversation to load.
  install  Creating a secret api key for the chatbot.
```

### New

Start a new conversation:

```sh
terminalgpt new
```

### Load

Load previous conversations:

```sh
terminalgpt load
```

### Delete

Delete previous conversations:

```sh
terminalgpt delete
```

### Using flags

Using flags, you can set the token limit and debug mode. the flags should be used before the command.

For example:

```sh
terminalgpt --token-limit 2048 --debug new
```

---

## Future Plans

1. Support multiline input.
2. Support optional vim input mode.
3. Auto-completion for all commands.
4. Open source the project.
5. Add more models (???)
6. Encrypt the conversation data.
7. Migrating to [Typer](https://typer.tiangolo.com/)
