"""Tests for printer.py."""

import unittest
from unittest.mock import patch

from terminalgpt.printer import (MarkdownPrinter, PlainPrinter, Printer,
                                 PrinterFactory, PrintUtils)


class TestPrintUtils_1(unittest.TestCase):
    """Tests for print_utils.py."""

    def set_test(self) -> tuple[Printer, Printer]:
        plain = PrinterFactory.get_printer("plain")
        markdown = PrinterFactory.get_printer("markdown")

        return plain, markdown

    def test_empty_string(self):
        """Tests empty string."""
        _, markdown = self.set_test()
        self.assertEqual(markdown._split_highlighted_string(""), [""])

    def test_no_highlighted_blocks(self):
        """Tests string with no highlighted blocks."""

        _, markdown = self.set_test()

        input_str = "This is a test string without any highlighted blocks."
        self.assertEqual(markdown._split_highlighted_string(input_str), [input_str])

    def test_single_highlighted_block(self):
        """Tests string with a single highlighted block."""
        plain, markdown = self.set_test()

        input_str = "This is a test string with a ```highlighted block``` in it."
        expected_output = [
            "This is a test string with a ",
            "```highlighted block```",
            " in it.",
        ]
        self.assertEqual(markdown._split_highlighted_string(input_str), expected_output)

    def test_multiple_highlighted_blocks(self):
        """Tests string with multiple highlighted blocks."""

        _, markdown = self.set_test()
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
        self.assertEqual(markdown._split_highlighted_string(input_str), expected_output)

    def test_adjacent_highlighted_blocks(self):
        """Tests string with adjacent highlighted blocks."""

        _, markdown = self.set_test()
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
        self.assertEqual(markdown._split_highlighted_string(input_str), expected_output)


from unittest import TestCase
from unittest.mock import MagicMock, patch

from terminalgpt.printer import (MarkdownPrinter, PlainPrinter, Printer,
                                 PrinterFactory, PrintUtils)


class TestPrinter(TestCase):
    """Tests for the Printer abstract base class."""

    def test_printt(self):
        """Tests the abstract printt method."""
        with self.assertRaises(TypeError):
            Printer().printt("Test")

    def test_print_assistant_message(self):
        """Tests the abstract print_assistant_message method."""
        with self.assertRaises(TypeError):
            Printer().print_assistant_message("Test")


class TestPlainPrinter(TestCase):
    """Tests for the PlainPrinter class."""

    def setUp(self):
        self.printer = PlainPrinter()

    @patch("builtins.print")
    def test_printt(self, mock_print):
        """Tests the printt method."""
        self.printer.printt("Test")
        mock_print.assert_called()

    @patch("builtins.print")
    def test_print_assistant_message(self, mock_print):
        """Tests the print_assistant_message method."""
        self.printer.print_assistant_message("Test")
        mock_print.assert_called()


class TestMarkdownPrinter(TestCase):
    """Tests for the MarkdownPrinter class."""

    def setUp(self):
        self.printer = MarkdownPrinter()

    @patch("builtins.print")
    def test_printt(self, mock_print):
        """Tests the printt method."""
        self.printer.printt("Test")
        mock_print.assert_called()

    @patch("builtins.print")
    def test_print_assistant_message(self, mock_print):
        """Tests the print_assistant_message method."""
        self.printer.print_assistant_message("Test")
        mock_print.assert_called()

    @patch("builtins.print")
    def test_print_with_delay(self, mock_print):
        """Tests the _print_with_delay method."""
        self.printer._print_with_delay("Test", 0.007)
        mock_print.assert_called()


class TestPrinterFactory(TestCase):
    """Tests for the PrinterFactory class."""

    def test_get_printer(self):
        """Tests the get_printer method."""
        self.assertIsInstance(PrinterFactory.get_printer("plain"), PlainPrinter)
        self.assertIsInstance(PrinterFactory.get_printer("markdown"), MarkdownPrinter)


class TestPrintUtils(TestCase):
    """Tests for the PrintUtils class."""

    def test_choose_random_message(self):
        """Tests the choose_random_message method."""
        messages = ["Test1", "Test2", "Test3"]
        self.assertIn(PrintUtils.choose_random_message(messages), messages)
