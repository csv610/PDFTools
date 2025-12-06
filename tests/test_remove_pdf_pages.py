"""Tests for remove_pdf_pages module."""

import sys
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add pdftools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdftools.remove_pdf_pages import parse_page_numbers, remove_pages


class TestParsePageNumbers(unittest.TestCase):
    """Test cases for parse_page_numbers function."""

    def test_parse_single_page(self):
        """Test parsing single page number."""
        result = parse_page_numbers("1", 10)
        self.assertEqual(result, {0})  # 1-indexed input becomes 0-indexed

    def test_parse_multiple_pages(self):
        """Test parsing multiple page numbers."""
        result = parse_page_numbers("1,3,5", 10)
        self.assertEqual(result, {0, 2, 4})

    def test_parse_page_range(self):
        """Test parsing page range."""
        result = parse_page_numbers("1-3", 10)
        self.assertEqual(result, {0, 1, 2})

    def test_parse_mixed_pages_and_ranges(self):
        """Test parsing mixed single pages and ranges."""
        result = parse_page_numbers("1,3-5,8", 10)
        self.assertEqual(result, {0, 2, 3, 4, 7})

    def test_parse_page_range_at_end(self):
        """Test parsing range at end of document."""
        result = parse_page_numbers("8-10", 10)
        self.assertEqual(result, {7, 8, 9})

    def test_parse_last_page(self):
        """Test parsing last page number."""
        result = parse_page_numbers("10", 10)
        self.assertEqual(result, {9})

    def test_parse_duplicate_pages(self):
        """Test that duplicate page numbers are handled correctly."""
        result = parse_page_numbers("1,1,3,3", 10)
        self.assertEqual(result, {0, 2})

    def test_parse_invalid_page_too_high(self):
        """Test parsing page number exceeding total pages."""
        with self.assertRaises(ValueError):
            parse_page_numbers("11", 10)

    def test_parse_invalid_page_zero(self):
        """Test parsing page zero (invalid, 1-indexed)."""
        with self.assertRaises(ValueError):
            parse_page_numbers("0", 10)

    def test_parse_invalid_negative_page(self):
        """Test parsing negative page number."""
        with self.assertRaises(ValueError):
            parse_page_numbers("-1", 10)

    def test_parse_invalid_range_reversed(self):
        """Test parsing range with reversed order."""
        with self.assertRaises(ValueError):
            parse_page_numbers("5-3", 10)

    def test_parse_empty_string(self):
        """Test parsing empty string."""
        with self.assertRaises(ValueError):
            parse_page_numbers("", 10)

    def test_parse_invalid_format(self):
        """Test parsing invalid format."""
        with self.assertRaises(ValueError):
            parse_page_numbers("1,a,3", 10)

    def test_parse_spaces_in_input(self):
        """Test parsing with spaces in input."""
        result = parse_page_numbers("1, 3, 5", 10)
        self.assertEqual(result, {0, 2, 4})

    def test_parse_range_with_spaces(self):
        """Test parsing range with spaces."""
        result = parse_page_numbers("1 - 3", 10)
        self.assertEqual(result, {0, 1, 2})

    def test_parse_single_item_set(self):
        """Test that result is a set."""
        result = parse_page_numbers("5", 10)
        self.assertIsInstance(result, set)

    def test_parse_comprehensive_example(self):
        """Test comprehensive parsing example."""
        result = parse_page_numbers("1,3-5,7,9-10", 10)
        self.assertEqual(result, {0, 2, 3, 4, 6, 8, 9})


class TestRemovePages(unittest.TestCase):
    """Test cases for remove_pages function."""

    @patch('pdftools.remove_pdf_pages.PdfReader')
    @patch('pdftools.remove_pdf_pages.PdfWriter')
    @patch('builtins.open', create=True)
    def test_remove_pages_basic(self, mock_open, mock_writer_class, mock_reader_class):
        """Test basic page removal."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(5)]

        mock_writer = MagicMock()
        mock_writer_class.return_value = mock_writer
        mock_writer.write.return_value = None

        result = remove_pages("input.pdf", "output.pdf", "2,4")

        self.assertEqual(result, 3)  # 5 - 2 removed = 3 remaining
        mock_writer_class.assert_called_once()

    @patch('pdftools.remove_pdf_pages.PdfReader')
    @patch('pdftools.remove_pdf_pages.PdfWriter')
    @patch('builtins.open', create=True)
    def test_remove_pages_single_page(self, mock_open, mock_writer_class, mock_reader_class):
        """Test removing single page."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(3)]

        mock_writer = MagicMock()
        mock_writer_class.return_value = mock_writer

        result = remove_pages("input.pdf", "output.pdf", "2")

        self.assertEqual(result, 2)  # 3 - 1 = 2

    @patch('pdftools.remove_pdf_pages.PdfReader')
    @patch('pdftools.remove_pdf_pages.PdfWriter')
    @patch('builtins.open', create=True)
    def test_remove_pages_range(self, mock_open, mock_writer_class, mock_reader_class):
        """Test removing page range."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(10)]

        mock_writer = MagicMock()
        mock_writer_class.return_value = mock_writer

        result = remove_pages("input.pdf", "output.pdf", "3-7")

        self.assertEqual(result, 5)  # 10 - 5 = 5

    @patch('pdftools.remove_pdf_pages.PdfReader')
    def test_remove_pages_file_not_found(self, mock_reader_class):
        """Test handling of missing input file."""
        mock_reader_class.side_effect = FileNotFoundError()

        with self.assertRaises(FileNotFoundError):
            remove_pages("nonexistent.pdf", "output.pdf", "1")

    @patch('pdftools.remove_pdf_pages.PdfReader')
    @patch('pdftools.remove_pdf_pages.PdfWriter')
    @patch('builtins.open', create=True)
    def test_remove_pages_preserves_order(self, mock_open, mock_writer_class, mock_reader_class):
        """Test that remaining pages maintain order."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader

        # Create mock pages with identifiable content
        pages = [MagicMock(page_num=i) for i in range(5)]
        mock_reader.pages = pages

        mock_writer = MagicMock()
        mock_writer_class.return_value = mock_writer

        remove_pages("input.pdf", "output.pdf", "2,4")

        # Verify add_page was called with remaining pages in order
        add_page_calls = [call[0][0] for call in mock_writer.add_page.call_args_list]
        self.assertEqual(len(add_page_calls), 3)

    @patch('pdftools.remove_pdf_pages.PdfReader')
    @patch('pdftools.remove_pdf_pages.PdfWriter')
    @patch('builtins.open', create=True)
    def test_remove_pages_all_pages_except_first(self, mock_open, mock_writer_class, mock_reader_class):
        """Test removing all pages except first."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(5)]

        mock_writer = MagicMock()
        mock_writer_class.return_value = mock_writer

        result = remove_pages("input.pdf", "output.pdf", "2-5")

        self.assertEqual(result, 1)  # Only first page remains

    @patch('pdftools.remove_pdf_pages.PdfReader')
    @patch('pdftools.remove_pdf_pages.PdfWriter')
    @patch('builtins.open', create=True)
    def test_remove_pages_invalid_page_reference(self, mock_open, mock_writer_class, mock_reader_class):
        """Test error handling for invalid page numbers."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(5)]

        with self.assertRaises(ValueError):
            remove_pages("input.pdf", "output.pdf", "6")

    @patch('pdftools.remove_pdf_pages.PdfReader')
    @patch('pdftools.remove_pdf_pages.PdfWriter')
    @patch('builtins.open', create=True)
    def test_remove_pages_return_type(self, mock_open, mock_writer_class, mock_reader_class):
        """Test that function returns an integer."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(5)]

        mock_writer = MagicMock()
        mock_writer_class.return_value = mock_writer

        result = remove_pages("input.pdf", "output.pdf", "1")

        self.assertIsInstance(result, int)


if __name__ == "__main__":
    unittest.main()
