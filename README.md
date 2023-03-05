# TerminalGPT

Welcome to terminalGPT, the terminal-based ChatGPT personal assistant app! With terminalGPT, you can easily interact with ChatGPT and receive short, easy-to-read answers on your terminal.

terminalGPT is specifically optimized for your machine's operating system, distribution, and chipset architecture, so you can be sure that the information and assistance you receive are tailored to your specific setup.

Whether you need help with a quick question or want to explore a complex topic, TerminalGPT is here to assist you. Simply enter your query and TerminalGPT will provide you with the best answer possible based on its extensive knowledge base.

Thank you for using TerminalGPT, and we hope you find the terminal-based app to be a valuable resource for your day-to-day needs!

# Pre-requisites

1. Python 3.9 or higher
2. [An OpenAI Account and API key](https://elephas.app/blog/how-to-create-openai-api-keys-cl5c4f21d281431po7k8fgyol0) that you can get for free with a limited quota.

# Installation

1. Install the package with pip install.

```sh
pip install terminalgpt -U
```

1. Replace `<YOUR_OPENAI_KEY>` below with your OpenAI API key. You can get one [here](https://beta.openai.com/account/api-keys).

```sh
export OPENAI_API_KEY=<YOUR_OPENAI_KEY>
git clone https://github.com/adamyodinsky/TerminalGPT.git
cd TerminalGPT
./inject_token.sh
```

*This step is optional but very recommended as it saves you the trouble of exporting your OpenAI API key every time you open a new terminal session.*

---

## Usage

![Alt Text](./usage.gif)


