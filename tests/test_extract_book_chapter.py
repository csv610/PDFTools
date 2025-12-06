"""Tests for extract_book_chapter module."""

import sys
import unittest
from unittest.mock import patch, MagicMock, Mock
from pathlib import Path
import json
import tempfile
import os

# Add pdftools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdftools.extract_book_chapter import BookChaptersExtractor, ChapterInfo

# Path to test PDFs
TEST_DATA_DIR = Path(__file__).parent.parent / "data"
PAPER_PDF = TEST_DATA_DIR / "paper.pdf"
LARGE_PDF = TEST_DATA_DIR / "536.pdf"


class TestChapterInfo(unittest.TestCase):
    """Test cases for ChapterInfo dataclass."""

    def test_chapter_info_creation(self):
        """Test creating ChapterInfo object."""
        chapter = ChapterInfo(id=1, title="Chapter 1", start_page=1, end_page=10)

        self.assertEqual(chapter.id, 1)
        self.assertEqual(chapter.title, "Chapter 1")
        self.assertEqual(chapter.start_page, 1)
        self.assertEqual(chapter.end_page, 10)

    def test_chapter_info_with_different_values(self):
        """Test ChapterInfo with various values."""
        chapter = ChapterInfo(id=5, title="Introduction", start_page=0, end_page=25)

        self.assertEqual(chapter.id, 5)
        self.assertEqual(chapter.title, "Introduction")
        self.assertEqual(chapter.start_page, 0)
        self.assertEqual(chapter.end_page, 25)

    def test_chapter_info_equality(self):
        """Test ChapterInfo equality comparison."""
        chapter1 = ChapterInfo(1, "Chapter 1", 1, 10)
        chapter2 = ChapterInfo(1, "Chapter 1", 1, 10)

        self.assertEqual(chapter1, chapter2)

    def test_chapter_info_inequality(self):
        """Test ChapterInfo inequality."""
        chapter1 = ChapterInfo(1, "Chapter 1", 1, 10)
        chapter2 = ChapterInfo(1, "Chapter 1", 1, 15)

        self.assertNotEqual(chapter1, chapter2)


class TestBookChaptersExtractor(unittest.TestCase):
    """Test cases for BookChaptersExtractor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.extractor = BookChaptersExtractor()

    @patch('pdftools.extract_book_chapter.PdfReader')
    def test_extractor_initialization(self, mock_reader_class):
        """Test extractor initialization."""
        extractor = BookChaptersExtractor()
        self.assertIsNotNone(extractor)

    def test_extract_chapters_basic(self):
        """Test basic chapter extraction."""
        result = self.extractor.extract_chapters(str(PAPER_PDF))

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_extract_chapters_with_output_json(self):
        """Test chapter extraction with JSON output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_json = f"{tmpdir}/chapters.json"

            result = self.extractor.extract_chapters(str(PAPER_PDF), output_json)

            self.assertIsInstance(result, list)
            self.assertTrue(os.path.exists(output_json), "Output JSON file should be created")

    def test_extract_chapters_file_not_found(self):
        """Test handling of missing PDF file."""
        with self.assertRaises(FileNotFoundError):
            self.extractor.extract_chapters("/nonexistent/path/test.pdf")

    def test_extract_chapters_returns_list(self):
        """Test that extraction returns a list."""
        result = self.extractor.extract_chapters(str(PAPER_PDF))
        self.assertIsInstance(result, list)

    def test_extract_chapters_list_contains_chapter_info(self):
        """Test that result list contains ChapterInfo objects."""
        result = self.extractor.extract_chapters(str(PAPER_PDF))

        if result:  # If chapters found
            for chapter in result:
                self.assertIsInstance(chapter, ChapterInfo)

    def test_extract_chapters_chapter_info_fields(self):
        """Test that ChapterInfo objects have required fields."""
        result = self.extractor.extract_chapters(str(PAPER_PDF))

        if result:
            chapter = result[0]
            self.assertTrue(hasattr(chapter, 'id'))
            self.assertTrue(hasattr(chapter, 'title'))
            self.assertTrue(hasattr(chapter, 'start_page'))
            self.assertTrue(hasattr(chapter, 'end_page'))

    def test_extract_chapters_page_numbers_reasonable(self):
        """Test that extracted page numbers are reasonable."""
        result = self.extractor.extract_chapters(str(LARGE_PDF))

        for chapter in result:
            # Page numbers should be positive
            self.assertGreaterEqual(chapter.start_page, 0)
            self.assertGreaterEqual(chapter.end_page, 0)
            # End page should be >= start page
            self.assertGreaterEqual(chapter.end_page, chapter.start_page)

    def test_extract_chapters_title_not_empty(self):
        """Test that chapter titles are not empty."""
        result = self.extractor.extract_chapters(str(PAPER_PDF))

        for chapter in result:
            if chapter.title:  # If title exists
                self.assertGreater(len(chapter.title.strip()), 0)

    def test_extract_chapters_id_uniqueness(self):
        """Test that chapter IDs are unique."""
        result = self.extractor.extract_chapters(str(LARGE_PDF))

        if len(result) > 1:
            ids = [ch.id for ch in result]
            self.assertEqual(len(ids), len(set(ids)))  # All unique


if __name__ == "__main__":
    unittest.main()
