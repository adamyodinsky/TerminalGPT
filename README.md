# ![TerminalGPT](logo.png)

[![Continuous Integration](https://github.com/adamyodinsky/TerminalGPT/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/adamyodinsky/TerminalGPT/actions/workflows/main.yml) ![PyPI](https://img.shields.io/pypi/v/terminalgpt) ![PyPI - Downloads](https://img.shields.io/pypi/dm/terminalgpt) ![commits-since](https://img.shields.io/github/commits-since/adamyodinsky/TerminalGPT/latest) ![GitHub last commit](https://img.shields.io/github/last-commit/adamyodinsky/terminalgpt)

Welcome to terminalGPT, the terminal-based ChatGPT personal assistant app!
With terminalGPT, you can easily interact with the OpenAI GPT 3.5 language model.

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
- An OpenAI Account and API key (It's free for personal use).
   1. Sign up at <https://beta.openai.com/signup> using email or Google/Microsoft account.
   2. Go to <https://beta.openai.com/account/api-keys> or click on "View API keys" in the menu to get your API key.

   (For a more detailed guide on how to create an OpenAI API key, click [here](https://elephas.app/blog/how-to-create-openai-api-keys-cl5c4f21d281431po7k8fgyol0).)

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

---

## Future Plans

1. Support optional vim input mode.
2. Auto-completion for all commands.
3. Add more models
4. Encrypt the conversation data.
5. GPT-4 support.

---
