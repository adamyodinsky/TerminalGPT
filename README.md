# ![TerminalGPT](logo.png)

[![Continuous Integration](https://github.com/adamyodinsky/TerminalGPT/actions/workflows/MainCI.yml/badge.svg?branch=main)](https://github.com/adamyodinsky/TerminalGPT/actions/workflows/main.yml) ![PyPI](https://img.shields.io/pypi/v/terminalgpt) ![PyPI - Downloads](https://img.shields.io/pypi/dm/terminalgpt) ![commits-since](https://img.shields.io/github/commits-since/adamyodinsky/TerminalGPT/latest) ![GitHub last commit](https://img.shields.io/github/last-commit/adamyodinsky/terminalgpt)

Welcome to terminalGPT, the terminal-based ChatGPT personal assistant app!
With terminalGPT, you can easily interact with the OpenAI GPT-3.5 and GPT-4 language models.

Whether you need help with a quick question or want to explore a complex topic, TerminalGPT is here to assist you. Simply enter your query and TerminalGPT will provide you with the best answer possible based on its extensive knowledge base.

---

<img width="910" alt="image" src="https://user-images.githubusercontent.com/27074934/229319537-f332923d-f92e-4d91-8d5e-d26d8997341e.png">

---

## Why?

Some advantages of using TerminalGPT over the chatGPT browser-based app:

- It doesn't disconnect like the browser-based app, so you can leave it running in a terminal session on the side without losing context.
- It's highly available and can be used whenever you need it.
- It's faster with replies than the browser-based app.
- You can use TerminalGPT with your IDE terminal, which means you won't have to constantly switch between your browser and your IDE when you have questions.
- TerminalGPT's answers are tailored to your machine's operating system, distribution, and chip-set architecture
- Doesn't use your conversation data for training the model (unlike the browser-based app).
- Your conversations are stored locally on your machine, so only you can access them.

## Pre-requisites

- Python 3.6 or higher
- An OpenAI Account and API key.
   1. Sign up at <https://beta.openai.com/signup> using email or Google/Microsoft account.
   2. Go to <https://beta.openai.com/account/api-keys> or click on "View API keys" in the menu to get your API key.

**Notes:** OpenAI FREE API trial expired on 01-04-2023. You can still use the API, but you will need to set up a payment method.

- To set up a payment method [click here](https://platform.openai.com/account/billing/payment-methods).
- To check your usage [click here](https://platform.openai.com/account/usage).
- To check pricing [click here](https://openai.com/pricing#language-models).

## Installation

1. Install the latest TerminalGPT with pip install.

```sh
pip install terminalgpt -U --user
```

2. Now you have `terminalgpt` command available in your terminal. Run the following install command to configure the app.

```sh
terminalgpt install
```

3. Enter your OpenAI API key when prompted and press enter.

That's it! You're ready to use TerminalGPT!

---

## Usage

### TL;DR

```sh
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  *~ TerminalGPT - Your Personal Terminal Assistant ~*

Options:
  --version                       Show the version and exit.
  -m, --model [gpt-3.5-turbo|gpt-4]
                                  Choose a model to use.  [default:
                                  gpt-3.5-turbo]
  -p, --plain                     Plain text output.
  --help                          Show this message and exit.

Commands:
  delete    Choose a previous conversation to load.
  install   Creating a secret api key for the chatbot.
  load      Choose a previous conversation to load.
  new       Start a new conversation.
  one-shot  One shot question answer.
```

### New

Start a new conversation:

```sh
terminalgpt new
```

### One-Shot

One shot question to get a fast answer in the terminal.

```sh
terminalgpt one-shot "What is the meaning of life?"
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

---

## Future Plans

1. Support optional Vim input mode.
2. Auto-completion for all commands.
3. Support local models

---
