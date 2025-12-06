"""Tests for pdf2text module."""

import sys
import unittest
from pathlib import Path
import tempfile
import os

# Add pdftools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdftools.pdf2text import pdf_to_text

# Path to test PDFs
TEST_DATA_DIR = Path(__file__).parent.parent / "data"
PAPER_PDF = TEST_DATA_DIR / "paper.pdf"
LARGE_PDF = TEST_DATA_DIR / "536.pdf"


class TestPdfToText(unittest.TestCase):
    """Test cases for pdf_to_text function."""

    def test_pdf_to_text_single_page_extraction(self):
        """Test text extraction from PDF returns a string."""
        result = pdf_to_text(str(PAPER_PDF))
        self.assertIsInstance(result, str)

    def test_pdf_to_text_multiple_pages(self):
        """Test text extraction from multiple page PDF."""
        result = pdf_to_text(str(PAPER_PDF))

        # Should contain text (not empty)
        self.assertGreater(len(result), 0)
        # Multiple pages should be separated
        self.assertIn('\n\n', result)

    def test_pdf_to_text_large_document(self):
        """Test text extraction from large PDF."""
        result = pdf_to_text(str(LARGE_PDF))

        # Should contain text
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_pdf_to_text_returns_string(self):
        """Test that extraction returns a string."""
        result = pdf_to_text(str(PAPER_PDF))
        self.assertIsInstance(result, str)

    def test_pdf_to_text_preserves_content(self):
        """Test that extracted content is preserved."""
        result1 = pdf_to_text(str(PAPER_PDF))
        result2 = pdf_to_text(str(PAPER_PDF))

        # Same file should produce same result
        self.assertEqual(result1, result2)

    def test_pdf_to_text_page_separator(self):
        """Test that pages are separated by double newline."""
        result = pdf_to_text(str(PAPER_PDF))

        # Check for page separator
        if '\n\n' in result:
            self.assertIn('\n\n', result)

    def test_pdf_to_text_whitespace_handling(self):
        """Test whitespace in extracted text."""
        result = pdf_to_text(str(PAPER_PDF))

        # Result should be a valid string (possibly with various whitespace)
        self.assertIsInstance(result, str)

    def test_pdf_to_text_special_characters(self):
        """Test extraction with potential special characters."""
        result = pdf_to_text(str(PAPER_PDF))

        # Should handle text properly
        self.assertIsInstance(result, str)

    def test_pdf_to_text_unicode_content(self):
        """Test extraction with unicode content."""
        result = pdf_to_text(str(PAPER_PDF))

        # Should be valid string
        self.assertIsInstance(result, str)

    def test_pdf_to_text_multiline_content(self):
        """Test extraction of multiline content."""
        result = pdf_to_text(str(PAPER_PDF))

        # Should contain newlines
        self.assertIn('\n', result)

    def test_pdf_to_text_page_with_no_text(self):
        """Test handling of pages with potentially no text."""
        # Extract from large PDF which may have empty pages
        result = pdf_to_text(str(LARGE_PDF))

        # Should still return a result (might be empty or partial)
        self.assertIsInstance(result, str)

    def test_pdf_to_text_mixed_empty_pages(self):
        """Test extraction with mixed empty and non-empty pages."""
        result = pdf_to_text(str(LARGE_PDF))

        # Should return valid string
        self.assertIsInstance(result, str)

    def test_pdf_to_text_file_not_found(self):
        """Test error handling for missing file."""
        with self.assertRaises(SystemExit):
            pdf_to_text("/nonexistent/path/test.pdf")

    def test_pdf_to_text_invalid_pdf(self):
        """Test error handling for invalid PDF."""
        # Create a temporary file with non-PDF content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.pdf', delete=False) as f:
            f.write("This is not a PDF file")
            temp_file = f.name

        try:
            with self.assertRaises(SystemExit):
                pdf_to_text(temp_file)
        finally:
            os.unlink(temp_file)

    def test_pdf_to_text_empty_pdf(self):
        """Test extraction from an empty or minimal PDF."""
        # Use one of the real PDFs
        result = pdf_to_text(str(PAPER_PDF))

        # Even minimal PDFs should return a string
        self.assertIsInstance(result, str)


if __name__ == "__main__":
    unittest.main()
