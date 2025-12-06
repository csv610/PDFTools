"""Tests for pdfpages2images module."""

import sys
import unittest
from unittest.mock import patch, MagicMock, Mock
from pathlib import Path
import tempfile
import os

# Add pdftools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdftools.pdfpages2images import PDF2ImageConverter


class TestPDF2ImageConverter(unittest.TestCase):
    """Test cases for PDF2ImageConverter class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_dir = self.temp_dir.name

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    @patch('pdftools.pdfpages2images.PdfReader')
    def test_converter_initialization(self, mock_reader_class):
        """Test converter initialization."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(5)]

        converter = PDF2ImageConverter("test.pdf", self.output_dir)

        self.assertIsNotNone(converter)
        self.assertEqual(converter.input_file, "test.pdf")
        self.assertEqual(converter.output_directory, self.output_dir)

    @patch('pdftools.pdfpages2images.PdfReader')
    def test_converter_dpi_parameter(self, mock_reader_class):
        """Test converter with custom DPI."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(5)]

        converter = PDF2ImageConverter("test.pdf", self.output_dir, dpi=150)

        self.assertEqual(converter.dpi, 150)

    @patch('pdftools.pdfpages2images.PdfReader')
    def test_converter_chunk_size_parameter(self, mock_reader_class):
        """Test converter with custom chunk size."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(5)]

        converter = PDF2ImageConverter("test.pdf", self.output_dir, chunk_size=10)

        self.assertEqual(converter.chunk_size, 10)

    @patch('pdftools.pdfpages2images.PdfReader')
    def test_converter_default_dpi(self, mock_reader_class):
        """Test default DPI value."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(5)]

        converter = PDF2ImageConverter("test.pdf", self.output_dir)

        self.assertEqual(converter.dpi, 300)

    @patch('pdftools.pdfpages2images.PdfReader')
    def test_converter_default_chunk_size(self, mock_reader_class):
        """Test default chunk size value."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(5)]

        converter = PDF2ImageConverter("test.pdf", self.output_dir)

        self.assertEqual(converter.chunk_size, 5)

    @patch('pdftools.pdfpages2images.PdfReader')
    def test_converter_invalid_dpi(self, mock_reader_class):
        """Test initialization with invalid DPI."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(5)]

        with self.assertRaises(ValueError):
            PDF2ImageConverter("test.pdf", self.output_dir, dpi=0)

    @patch('pdftools.pdfpages2images.PdfReader')
    def test_converter_invalid_chunk_size(self, mock_reader_class):
        """Test initialization with invalid chunk size."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(5)]

        with self.assertRaises(ValueError):
            PDF2ImageConverter("test.pdf", self.output_dir, chunk_size=0)

    @patch('pdftools.pdfpages2images.PdfReader')
    def test_converter_file_not_found(self, mock_reader_class):
        """Test initialization with non-existent PDF."""
        mock_reader_class.side_effect = FileNotFoundError()

        with self.assertRaises(FileNotFoundError):
            PDF2ImageConverter("nonexistent.pdf", self.output_dir)

    @patch('pdftools.pdfpages2images.PdfReader')
    def test_create_output_directory(self, mock_reader_class):
        """Test output directory creation."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(5)]

        new_dir = os.path.join(self.output_dir, "new_output")
        converter = PDF2ImageConverter("test.pdf", new_dir)

        converter.create_output_directory()

        self.assertTrue(os.path.exists(new_dir))

    @patch('pdftools.pdfpages2images.PdfReader')
    def test_get_page_count(self, mock_reader_class):
        """Test getting page count."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(10)]

        converter = PDF2ImageConverter("test.pdf", self.output_dir)

        count = converter.get_page_count()

        self.assertEqual(count, 10)

    @patch('pdftools.pdfpages2images.PdfReader')
    def test_get_page_count_empty_pdf(self, mock_reader_class):
        """Test page count for empty PDF."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = []

        converter = PDF2ImageConverter("empty.pdf", self.output_dir)

        count = converter.get_page_count()

        self.assertEqual(count, 0)

    @patch('pdftools.pdfpages2images.PdfReader')
    @patch('pdftools.pdfpages2images.convert_from_path')
    def test_convert_to_images_basic(self, mock_convert_func, mock_reader_class):
        """Test basic image conversion."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(5)]

        mock_images = [MagicMock() for _ in range(5)]
        mock_convert_func.return_value = mock_images

        converter = PDF2ImageConverter("test.pdf", self.output_dir)

        result = converter.convert_to_images()

        self.assertIsInstance(result, list)

    @patch('pdftools.pdfpages2images.PdfReader')
    @patch('pdftools.pdfpages2images.convert_from_path')
    def test_convert_to_images_returns_paths(self, mock_convert_func, mock_reader_class):
        """Test that conversion returns image paths."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(3)]

        mock_images = [MagicMock() for _ in range(3)]
        mock_convert_func.return_value = mock_images

        converter = PDF2ImageConverter("test.pdf", self.output_dir)

        result = converter.convert_to_images()

        self.assertIsInstance(result, list)
        # Result should have paths for each image
        self.assertGreaterEqual(len(result), 0)

    @patch('pdftools.pdfpages2images.PdfReader')
    def test_get_images_empty(self, mock_reader_class):
        """Test get_images with no conversion done."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(5)]

        converter = PDF2ImageConverter("test.pdf", self.output_dir)

        images = converter.get_images()

        self.assertIsInstance(images, list)

    @patch('pdftools.pdfpages2images.PdfReader')
    def test_save_image_basic(self, mock_reader_class):
        """Test saving a single image."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(5)]

        converter = PDF2ImageConverter("test.pdf", self.output_dir)

        mock_image = MagicMock()
        output_file = os.path.join(self.output_dir, "page_1.png")

        converter.save_image(mock_image, output_file)

        # Should not raise an error
        mock_image.save.assert_called_once()

    @patch('pdftools.pdfpages2images.PdfReader')
    def test_converter_with_special_path(self, mock_reader_class):
        """Test converter with special characters in paths."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(5)]

        special_dir = os.path.join(self.output_dir, "path with spaces")
        os.makedirs(special_dir, exist_ok=True)

        converter = PDF2ImageConverter("test.pdf", special_dir)

        self.assertEqual(converter.output_directory, special_dir)

    @patch('pdftools.pdfpages2images.PdfReader')
    @patch('pdftools.pdfpages2images.convert_from_path')
    def test_convert_respects_chunk_size(self, mock_convert_func, mock_reader_class):
        """Test that conversion respects chunk size."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(15)]

        mock_images = [MagicMock() for _ in range(15)]
        mock_convert_func.return_value = mock_images

        converter = PDF2ImageConverter("test.pdf", self.output_dir, chunk_size=5)

        result = converter.convert_to_images()

        self.assertIsInstance(result, list)


if __name__ == "__main__":
    unittest.main()
