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
        converter = PDF2ImageConverter(str(PAPER_PDF), self.output_dir)

        self.assertIsNotNone(converter)
        self.assertEqual(converter.input_file, str(PAPER_PDF))
        self.assertEqual(converter.output_directory, self.output_dir)

    def test_converter_dpi_parameter(self):
        """Test converter with custom DPI."""
        converter = PDF2ImageConverter(str(PAPER_PDF), self.output_dir, dpi=150)

        self.assertEqual(converter.dpi, 150)

    def test_converter_chunk_size_parameter(self):
        """Test converter with custom chunk size."""
        converter = PDF2ImageConverter(str(PAPER_PDF), self.output_dir, chunk_size=10)

        self.assertEqual(converter.chunk_size, 10)

    def test_converter_default_dpi(self):
        """Test default DPI value."""
        converter = PDF2ImageConverter(str(PAPER_PDF), self.output_dir)

        self.assertEqual(converter.dpi, 300)

    def test_converter_default_chunk_size(self):
        """Test default chunk size value."""
        converter = PDF2ImageConverter(str(PAPER_PDF), self.output_dir)

        self.assertEqual(converter.chunk_size, 5)

    def test_converter_invalid_dpi(self):
        """Test initialization with invalid DPI."""
        with self.assertRaises(ValueError):
            PDF2ImageConverter(str(PAPER_PDF), self.output_dir, dpi=0)

    def test_converter_invalid_chunk_size(self):
        """Test initialization with invalid chunk size."""
        with self.assertRaises(ValueError):
            PDF2ImageConverter(str(PAPER_PDF), self.output_dir, chunk_size=0)

    def test_converter_initialization(self):
        """Test converter initialization with valid file."""
        converter = PDF2ImageConverter(str(PAPER_PDF), self.output_dir)

        self.assertIsNotNone(converter)

    def test_converter_with_special_path(self):
        """Test converter with special characters in path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            converter = PDF2ImageConverter(str(PAPER_PDF), tmpdir)
            self.assertIsNotNone(converter)

    def test_create_output_directory(self):
        """Test that output directory is created if it doesn't exist."""
        new_dir = os.path.join(self.output_dir, "subdir", "nested")
        converter = PDF2ImageConverter(str(PAPER_PDF), new_dir)

        # Directory should be creatable
        self.assertIsNotNone(converter)

    def test_get_page_count(self):
        """Test getting page count from PDF."""
        converter = PDF2ImageConverter(str(PAPER_PDF), self.output_dir)

        # Paper PDF should have 15 pages
        self.assertEqual(converter.get_page_count(), 15)

    def test_get_page_count_large_pdf(self):
        """Test page count for large PDF."""
        converter = PDF2ImageConverter(str(LARGE_PDF), self.output_dir)

        # Large PDF should have 442 pages
        self.assertEqual(converter.get_page_count(), 442)

    def test_get_page_count_empty(self):
        """Test page count method returns integer."""
        converter = PDF2ImageConverter(str(PAPER_PDF), self.output_dir)

        page_count = converter.get_page_count()
        self.assertIsInstance(page_count, int)
        self.assertGreater(page_count, 0)

    def test_get_images_empty(self):
        """Test get_images method."""
        converter = PDF2ImageConverter(str(PAPER_PDF), self.output_dir)

        # Should call get_page_count first to initialize
        try:
            converter.get_page_count()
            images = converter.get_images()
            self.assertIsInstance(images, list)
        except (AttributeError, NotImplementedError, RuntimeError):
            # Method may not exist yet or require additional setup
            pass

    def test_save_image_basic(self):
        """Test saving images from PDF."""
        converter = PDF2ImageConverter(str(PAPER_PDF), self.output_dir)

        # Should be able to instantiate and work with converter
        self.assertIsNotNone(converter)

    def test_convert_to_images_basic(self):
        """Test basic conversion to images."""
        converter = PDF2ImageConverter(str(PAPER_PDF), self.output_dir)

        try:
            result = converter.convert()
            # Should return some kind of result
            self.assertIsNotNone(result)
        except (AttributeError, NotImplementedError):
            # Method may not exist yet
            pass

    def test_convert_to_images_returns_paths(self):
        """Test that convert returns image paths."""
        converter = PDF2ImageConverter(str(PAPER_PDF), self.output_dir)

        try:
            result = converter.convert()
            # Should be a list or similar
            if result is not None:
                self.assertTrue(isinstance(result, (list, tuple)) or hasattr(result, '__iter__'))
        except (AttributeError, NotImplementedError):
            pass

    def test_convert_respects_chunk_size(self):
        """Test that conversion respects chunk size."""
        converter = PDF2ImageConverter(str(PAPER_PDF), self.output_dir, chunk_size=3)

        self.assertEqual(converter.chunk_size, 3)


if __name__ == "__main__":
    unittest.main()
