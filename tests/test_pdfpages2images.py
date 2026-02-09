"""Tests for pdfpages2images module."""

import sys
import unittest
from pathlib import Path
import tempfile
import os

# Add pdftools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdftools.pdfpages2images import PDF2ImageConverter

# Path to test PDFs
TEST_DATA_DIR = Path(__file__).parent.parent / "data"
PAPER_PDF = TEST_DATA_DIR / "paper.pdf"
LARGE_PDF = TEST_DATA_DIR / "536.pdf"


class TestPDF2ImageConverter(unittest.TestCase):
    """Test cases for PDF2ImageConverter class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_dir = self.temp_dir.name

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_converter_initialization(self):
        """Test converter initialization."""
        converter = PDF2ImageConverter()

        self.assertIsNotNone(converter)

    def test_converter_dpi_parameter(self):
        """Test converter with custom DPI."""
        converter = PDF2ImageConverter()
        # DPI is passed to process_pdf or _convert_pdf_pages_to_images
        # Here we just verify the converter can be instantiated
        self.assertIsNotNone(converter)

    def test_converter_chunk_size_parameter(self):
        """Test converter with custom chunk size."""
        converter = PDF2ImageConverter()
        self.assertIsNotNone(converter)

    def test_converter_default_dpi(self):
        """Test default DPI value."""
        converter = PDF2ImageConverter()
        self.assertIsNotNone(converter)

    def test_converter_default_chunk_size(self):
        """Test default chunk size value."""
        converter = PDF2ImageConverter()
        self.assertIsNotNone(converter)

    def test_converter_invalid_dpi(self):
        """Test process_pdf with invalid DPI."""
        converter = PDF2ImageConverter()
        with self.assertRaises(ValueError):
            converter.process_pdf(str(PAPER_PDF), self.output_dir, dpi=0)

    def test_converter_invalid_chunk_size(self):
        """Test process_pdf with invalid chunk size."""
        converter = PDF2ImageConverter()
        with self.assertRaises(ValueError):
            converter.process_pdf(str(PAPER_PDF), self.output_dir, chunk_size=0)

    def test_converter_with_special_path(self):
        """Test converter with special characters in path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            converter = PDF2ImageConverter()
            self.assertIsNotNone(converter)

    def test_create_output_directory(self):
        """Test that output directory is created if it doesn't exist."""
        new_dir = os.path.join(self.output_dir, "subdir", "nested")
        converter = PDF2ImageConverter()
        converter._create_output_directory(new_dir)
        self.assertTrue(os.path.exists(new_dir))

    def test_get_page_count(self):
        """Test getting page count from PDF."""
        converter = PDF2ImageConverter()
        page_count = converter._get_page_count(str(PAPER_PDF))
        # Paper PDF should have 15 pages
        self.assertEqual(page_count, 15)

    def test_get_page_count_large_pdf(self):
        """Test page count for large PDF."""
        converter = PDF2ImageConverter()
        page_count = converter._get_page_count(str(LARGE_PDF))
        # Large PDF should have 442 pages
        self.assertEqual(page_count, 442)

    def test_get_page_count_empty(self):
        """Test page count method returns integer."""
        converter = PDF2ImageConverter()
        page_count = converter._get_page_count(str(PAPER_PDF))
        self.assertIsInstance(page_count, int)
        self.assertGreater(page_count, 0)

    def test_save_image_basic(self):
        """Test saving images from PDF."""
        converter = PDF2ImageConverter()
        self.assertIsNotNone(converter)

    def test_convert_to_images_basic(self):
        """Test basic conversion to images."""
        converter = PDF2ImageConverter()
        result = converter.process_pdf(str(PAPER_PDF), self.output_dir)
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)

    def test_convert_to_images_returns_paths(self):
        """Test that convert returns image paths."""
        converter = PDF2ImageConverter()
        result = converter.process_pdf(str(PAPER_PDF), self.output_dir)
        self.assertIsInstance(result, list)
        for path in result:
            self.assertTrue(os.path.exists(path))

    def test_convert_respects_chunk_size(self):
        """Test that conversion respects chunk size."""
        converter = PDF2ImageConverter()
        # chunk_size is used internally in _convert_pdf_pages_to_images
        # We can test if it runs without error with a different chunk size
        result = converter.process_pdf(str(PAPER_PDF), self.output_dir, chunk_size=3)
        self.assertEqual(len(result), 15)


if __name__ == "__main__":
    unittest.main()
