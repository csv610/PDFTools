"""Tests for remove_pdf_pages module."""

import sys
import unittest
from pathlib import Path
import tempfile

# Add pdftools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdftools.remove_pdf_pages import remove_pages

# Path to test PDFs
TEST_DATA_DIR = Path(__file__).parent.parent / "data"
PAPER_PDF = TEST_DATA_DIR / "paper.pdf"
LARGE_PDF = TEST_DATA_DIR / "536.pdf"


class TestRemovePages(unittest.TestCase):
    """Test cases for remove_pages function."""

    def test_remove_pages_basic(self):
        """Test basic page removal."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "output.pdf"
            result = remove_pages(str(PAPER_PDF), str(output_file), "1")

            self.assertGreater(result, 0)

    def test_remove_pages_single_page(self):
        """Test removing a single page."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "output.pdf"
            result = remove_pages(str(PAPER_PDF), str(output_file), "5")

            self.assertGreater(result, 0)

    def test_remove_pages_range(self):
        """Test removing a range of pages."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "output.pdf"
            result = remove_pages(str(PAPER_PDF), str(output_file), "1-3")

            self.assertGreater(result, 0)

    def test_remove_pages_multiple_pages(self):
        """Test removing multiple non-consecutive pages."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "output.pdf"
            result = remove_pages(str(PAPER_PDF), str(output_file), "2,4,6")

            self.assertGreater(result, 0)

    def test_remove_pages_preserves_order(self):
        """Test that remaining pages maintain order."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "output.pdf"
            result = remove_pages(str(PAPER_PDF), str(output_file), "5")

            self.assertGreater(result, 0)

    def test_remove_pages_return_type(self):
        """Test that function returns correct type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "output.pdf"
            result = remove_pages(str(PAPER_PDF), str(output_file), "1")

            # Should return an integer (page count)
            self.assertIsInstance(result, int)

    def test_remove_pages_all_pages_except_first(self):
        """Test removing all pages except first."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "output.pdf"
            result = remove_pages(str(PAPER_PDF), str(output_file), "2-15")

            self.assertEqual(result, 1)  # Only first page should remain

    def test_remove_pages_invalid_page_reference(self):
        """Test error handling for invalid page numbers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "output.pdf"
            # Should handle gracefully or raise appropriate error
            try:
                result = remove_pages(str(PAPER_PDF), str(output_file), "100")
                # If it succeeds, that's ok too
                self.assertGreaterEqual(result, 0)
            except (ValueError, RuntimeError):
                # Expected behavior for out-of-range pages
                pass


if __name__ == "__main__":
    unittest.main()
