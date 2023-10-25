"""Tests for chat_utils.py."""

import unittest

from terminalgpt import printer


class TestPrintUtils(unittest.TestCase):
    """Tests for print_utils.py."""

    def test_empty_string(self):
        """Tests empty string."""

        self.assertEqual(printer.split_highlighted_string(""), [""])

    def test_no_highlighted_blocks(self):
        """Tests string with no highlighted blocks."""

        input_str = "This is a test string without any highlighted blocks."
        self.assertEqual(printer.split_highlighted_string(input_str), [input_str])

    def test_single_highlighted_block(self):
        """Tests string with a single highlighted block."""

        input_str = "This is a test string with a ```highlighted block``` in it."
        expected_output = [
            "This is a test string with a ",
            "```highlighted block```",
            " in it.",
        ]
        self.assertEqual(printer.split_highlighted_string(input_str), expected_output)

    def test_multiple_highlighted_blocks(self):
        """Tests string with multiple highlighted blocks."""

        input_str = (
            "This is a test string with ```multiple``` highlighted ```blocks``` in it."
        )
        expected_output = [
            "This is a test string with ",
            "```multiple```",
            " highlighted ",
            "```blocks```",
            " in it.",
        ]
        self.assertEqual(printer.split_highlighted_string(input_str), expected_output)

    def test_adjacent_highlighted_blocks(self):
        """Tests string with adjacent highlighted blocks."""

        input_str = (
            "This is a test string with ```two``````adjacent``` highlighted blocks."
        )
        expected_output = [
            "This is a test string with ",
            "```two```",
            "",
            "```adjacent```",
            " highlighted blocks.",
        ]
        self.assertEqual(printer.split_highlighted_string(input_str), expected_output)
