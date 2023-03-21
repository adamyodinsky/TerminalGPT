"""Print utilities."""
import time


def print_slowly(text, delay=0.008):
    """Prints text slowly."""

    try:
        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
    except KeyboardInterrupt:
        print()
    finally:
        print()
