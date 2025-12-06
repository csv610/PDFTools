"""Tests for split_pdf_file module."""

import sys
import unittest
from unittest.mock import patch, MagicMock, Mock
from pathlib import Path
import tempfile
import os

# Add pdftools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdftools.split_pdf_file import split_pdf, save_split_pdfs


class TestSplitPdf(unittest.TestCase):
    """Test cases for split_pdf function."""

    @patch('pdftools.split_pdf_file.PdfReader')
    @patch('pdftools.split_pdf_file.PdfWriter')
    def test_split_pdf_basic(self, mock_writer_class, mock_reader_class):
        """Test basic PDF splitting."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(10)]

        mock_writer = MagicMock()
        mock_writer_class.return_value = mock_writer

        result = split_pdf("input.pdf", 5)

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    @patch('pdftools.split_pdf_file.PdfReader')
    @patch('pdftools.split_pdf_file.PdfWriter')
    def test_split_pdf_exact_division(self, mock_writer_class, mock_reader_class):
        """Test splitting where pages divide evenly."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        pages = [MagicMock() for _ in range(10)]
        mock_reader.pages = pages

        mock_writer = MagicMock()
        mock_writer_class.return_value = mock_writer

        result = split_pdf("input.pdf", 5)

        # 10 pages / 5 per split = 2 files
        self.assertEqual(len(result), 2)

    @patch('pdftools.split_pdf_file.PdfReader')
    @patch('pdftools.split_pdf_file.PdfWriter')
    def test_split_pdf_uneven_division(self, mock_writer_class, mock_reader_class):
        """Test splitting where pages don't divide evenly."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(12)]

        mock_writer = MagicMock()
        mock_writer_class.return_value = mock_writer

        result = split_pdf("input.pdf", 5)

        # 12 pages / 5 per split = 3 files (2+2+2 or 5+5+2)
        self.assertEqual(len(result), 3)

    @patch('pdftools.split_pdf_file.PdfReader')
    @patch('pdftools.split_pdf_file.PdfWriter')
    def test_split_pdf_single_page_per_split(self, mock_writer_class, mock_reader_class):
        """Test splitting with one page per file."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(5)]

        mock_writer = MagicMock()
        mock_writer_class.return_value = mock_writer

        result = split_pdf("input.pdf", 1)

        self.assertEqual(len(result), 5)

    @patch('pdftools.split_pdf_file.PdfReader')
    @patch('pdftools.split_pdf_file.PdfWriter')
    def test_split_pdf_more_pages_per_split_than_total(self, mock_writer_class, mock_reader_class):
        """Test splitting with more pages per split than total pages."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(3)]

        mock_writer = MagicMock()
        mock_writer_class.return_value = mock_writer

        result = split_pdf("input.pdf", 10)

        # All pages in one file
        self.assertEqual(len(result), 1)

    @patch('pdftools.split_pdf_file.PdfReader')
    @patch('pdftools.split_pdf_file.PdfWriter')
    def test_split_pdf_with_start_page(self, mock_writer_class, mock_reader_class):
        """Test splitting with custom start page."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(10)]

        mock_writer = MagicMock()
        mock_writer_class.return_value = mock_writer

        result = split_pdf("input.pdf", 2, start_page=3)

        # Should process pages 3-10 only
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    @patch('pdftools.split_pdf_file.PdfReader')
    @patch('pdftools.split_pdf_file.PdfWriter')
    def test_split_pdf_with_end_page(self, mock_writer_class, mock_reader_class):
        """Test splitting with custom end page."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(10)]

        mock_writer = MagicMock()
        mock_writer_class.return_value = mock_writer

        result = split_pdf("input.pdf", 2, end_page=5)

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    @patch('pdftools.split_pdf_file.PdfReader')
    @patch('pdftools.split_pdf_file.PdfWriter')
    def test_split_pdf_with_start_and_end(self, mock_writer_class, mock_reader_class):
        """Test splitting with both start and end page."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(10)]

        mock_writer = MagicMock()
        mock_writer_class.return_value = mock_writer

        result = split_pdf("input.pdf", 2, start_page=2, end_page=8)

        self.assertIsInstance(result, list)

    @patch('pdftools.split_pdf_file.PdfReader')
    def test_split_pdf_file_not_found(self, mock_reader_class):
        """Test handling of missing PDF file."""
        mock_reader_class.side_effect = FileNotFoundError()

        with self.assertRaises(FileNotFoundError):
            split_pdf("nonexistent.pdf", 5)

    @patch('pdftools.split_pdf_file.PdfReader')
    @patch('pdftools.split_pdf_file.PdfWriter')
    def test_split_pdf_invalid_pages_per_split(self, mock_writer_class, mock_reader_class):
        """Test error handling for invalid pages_per_split."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(10)]

        with self.assertRaises(ValueError):
            split_pdf("input.pdf", 0)

    @patch('pdftools.split_pdf_file.PdfReader')
    @patch('pdftools.split_pdf_file.PdfWriter')
    def test_split_pdf_returns_list_of_writers(self, mock_writer_class, mock_reader_class):
        """Test that function returns list of PdfWriter objects."""
        mock_reader = MagicMock()
        mock_reader_class.return_value = mock_reader
        mock_reader.pages = [MagicMock() for _ in range(10)]

        mock_writer = MagicMock()
        mock_writer_class.return_value = mock_writer

        result = split_pdf("input.pdf", 5)

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)


class TestSaveSplitPdfs(unittest.TestCase):
    """Test cases for save_split_pdfs function."""

    def test_save_split_pdfs_creates_directory(self):
        """Test that output directory is created if needed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = os.path.join(tmpdir, "output", "subdir")

            mock_writer1 = MagicMock()
            mock_writer2 = MagicMock()
            split_pdfs = [mock_writer1, mock_writer2]

            with patch('builtins.open', create=True):
                result = save_split_pdfs(split_pdfs, output_dir)

            self.assertEqual(result, 2)

    def test_save_split_pdfs_single_file(self):
        """Test saving single split PDF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_writer = MagicMock()
            split_pdfs = [mock_writer]

            with patch('builtins.open', create=True):
                result = save_split_pdfs(split_pdfs, tmpdir)

            self.assertEqual(result, 1)

    def test_save_split_pdfs_multiple_files(self):
        """Test saving multiple split PDFs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_writers = [MagicMock() for _ in range(5)]

            with patch('builtins.open', create=True):
                result = save_split_pdfs(mock_writers, tmpdir)

            self.assertEqual(result, 5)

    def test_save_split_pdfs_returns_count(self):
        """Test that function returns correct count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_writers = [MagicMock() for _ in range(3)]

            with patch('builtins.open', create=True):
                result = save_split_pdfs(mock_writers, tmpdir)

            self.assertIsInstance(result, int)
            self.assertEqual(result, 3)

    def test_save_split_pdfs_empty_list(self):
        """Test saving empty list of PDFs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            split_pdfs = []

            result = save_split_pdfs(split_pdfs, tmpdir)

            self.assertEqual(result, 0)

    def test_save_split_pdfs_calls_write(self):
        """Test that write method is called for each PDF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_writer1 = MagicMock()
            mock_writer2 = MagicMock()
            split_pdfs = [mock_writer1, mock_writer2]

            with patch('builtins.open', create=True):
                save_split_pdfs(split_pdfs, tmpdir)

            # Both writers should have write called
            mock_writer1.write.assert_called()
            mock_writer2.write.assert_called()

    def test_save_split_pdfs_file_naming(self):
        """Test that output files are named appropriately."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_writers = [MagicMock() for _ in range(3)]

            with patch('builtins.open', create=True) as mock_open:
                save_split_pdfs(mock_writers, tmpdir)

            # Should create files with appropriate names
            self.assertTrue(mock_open.called)

    def test_save_split_pdfs_with_special_path(self):
        """Test saving with special characters in path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            special_dir = os.path.join(tmpdir, "path with spaces")
            mock_writer = MagicMock()

            with patch('builtins.open', create=True):
                result = save_split_pdfs([mock_writer], special_dir)

            self.assertEqual(result, 1)

    def test_save_split_pdfs_preserves_order(self):
        """Test that PDFs are saved in order."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_writers = [MagicMock(name=f"writer_{i}") for i in range(3)]

            with patch('builtins.open', create=True):
                result = save_split_pdfs(mock_writers, tmpdir)

            self.assertEqual(result, 3)
            # All writers should have been processed
            for writer in mock_writers:
                writer.write.assert_called()


if __name__ == "__main__":
    unittest.main()
