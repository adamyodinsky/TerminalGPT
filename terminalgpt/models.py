import tiktoken
import openai


MODEL = "gpt-3.5-turbo"
ENCODING_MODEL = "gpt2"

TIKTOKEN_ENCODER = tiktoken.get_encoding(ENCODING_MODEL)

def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    num_tokens = len(TIKTOKEN_ENCODER.encode(string))
    return num_tokens

def get_answer(messages):
    answer = openai.ChatCompletion.create(
      model=MODEL,
      messages=messages
    )
    return answer
