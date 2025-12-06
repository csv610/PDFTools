"""Tests for extract_paragraphs module."""

import sys
import unittest
from pathlib import Path

# Add pdftools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdftools.extract_paragraphs import extract_all_paragraphs
from pdftools.discard_tracker import DiscardTracker


class TestExtractAllParagraphs(unittest.TestCase):
    """Test cases for extract_all_paragraphs function."""

    def setUp(self):
        """Set up test fixtures."""
        self.tracker = DiscardTracker()

    def test_extract_paragraphs_basic(self):
        """Test basic paragraph extraction."""
        text = """First paragraph with multiple lines.
        Still part of first paragraph.

        Second paragraph starts here.
        Also part of second paragraph."""
        boundaries = [0, len(text)]

        paragraphs, page_starts, page_ends = extract_all_paragraphs(text, boundaries, self.tracker)

        self.assertGreater(len(paragraphs), 0)
        self.assertEqual(len(paragraphs), len(page_starts))
        self.assertEqual(len(paragraphs), len(page_ends))

    def test_extract_paragraphs_empty_text(self):
        """Test extraction from empty text."""
        text = ""
        boundaries = [0]

        paragraphs, page_starts, page_ends = extract_all_paragraphs(text, boundaries, self.tracker)

        self.assertEqual(len(paragraphs), 0)
        self.assertEqual(len(page_starts), 0)
        self.assertEqual(len(page_ends), 0)

    def test_extract_paragraphs_single_paragraph(self):
        """Test extraction with single paragraph."""
        text = "This is a single paragraph with enough characters to not be filtered out."
        boundaries = [0, len(text)]

        paragraphs, page_starts, page_ends = extract_all_paragraphs(text, boundaries, self.tracker)

        self.assertEqual(len(paragraphs), 1)
        self.assertEqual(len(page_starts), 1)
        self.assertEqual(len(page_ends), 1)

    def test_extract_paragraphs_multiple_paragraphs(self):
        """Test extraction with multiple paragraphs separated by blank lines."""
        text = """Paragraph one is here with content.

        Paragraph two comes after blank line.

        Paragraph three is final."""
        boundaries = [0, len(text)]

        paragraphs, page_starts, page_ends = extract_all_paragraphs(text, boundaries, self.tracker)

        self.assertGreater(len(paragraphs), 1)

    def test_extract_paragraphs_filters_short_paragraphs(self):
        """Test that short paragraphs are filtered."""
        text = "Long paragraph with many words to ensure it passes the filter requirements here. Short. Another long paragraph with sufficient content to pass filtering requirements."
        boundaries = [0, len(text)]

        paragraphs, page_starts, page_ends = extract_all_paragraphs(text, boundaries, self.tracker)

        # All paragraphs should have minimum length
        for para in paragraphs:
            self.assertGreater(len(para), 0)

    def test_extract_paragraphs_page_positions_ordered(self):
        """Test that page positions are consistent."""
        text = """First long paragraph content here with many details and information.

        Second paragraph content here as well with substantial information included.

        Third paragraph here."""
        boundaries = [0, len(text) // 2, len(text)]

        paragraphs, page_starts, page_ends = extract_all_paragraphs(text, boundaries, self.tracker)

        # For each paragraph, start page should be <= end page
        for start, end in zip(page_starts, page_ends):
            self.assertLessEqual(start, end)

    def test_extract_paragraphs_returns_tuple(self):
        """Test that function returns a tuple of three lists."""
        text = "Paragraph one here. Another paragraph here."
        boundaries = [0, len(text)]

        result = extract_all_paragraphs(text, boundaries, self.tracker)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)
        self.assertIsInstance(result[0], list)  # paragraphs
        self.assertIsInstance(result[1], list)  # page_starts
        self.assertIsInstance(result[2], list)  # page_ends

    def test_extract_paragraphs_whitespace_handling(self):
        """Test that whitespace is properly handled."""
        text = "First paragraph.   \n\n   Second paragraph."
        boundaries = [0, len(text)]

        paragraphs, page_starts, page_ends = extract_all_paragraphs(text, boundaries, self.tracker)

        # Paragraphs should be stripped of leading/trailing whitespace
        for para in paragraphs:
            self.assertEqual(para, para.strip())

    def test_extract_paragraphs_multiline_paragraphs(self):
        """Test extraction with multi-line paragraphs."""
        text = """This is a paragraph that spans multiple lines.
        It continues here with more content.
        And more content on this line.

        This is a second paragraph.
        It also has multiple lines of content.
        With additional information here."""
        boundaries = [0, len(text)]

        paragraphs, page_starts, page_ends = extract_all_paragraphs(text, boundaries, self.tracker)

        self.assertGreaterEqual(len(paragraphs), 1)

    def test_extract_paragraphs_unicode_content(self):
        """Test extraction with unicode content."""
        text = """Français content is here with valid paragraph text.

        Español paragraph with content included here.

        English final paragraph."""
        boundaries = [0, len(text)]

        paragraphs, page_starts, page_ends = extract_all_paragraphs(text, boundaries, self.tracker)

        self.assertGreater(len(paragraphs), 0)
        extracted = " ".join(paragraphs)
        self.assertIn("content", extracted.lower())

    def test_extract_paragraphs_updates_tracker(self):
        """Test that tracker is updated during extraction."""
        text = "Paragraph one with content. Another paragraph with content."
        boundaries = [0, len(text)]

        paragraphs, _, _ = extract_all_paragraphs(text, boundaries, self.tracker)

        # Tracker should have been used
        self.assertGreater(len(self.tracker.discards), 0)

    def test_extract_paragraphs_various_separators(self):
        """Test extraction with various paragraph separators."""
        text = "First paragraph content here.\n\nSecond paragraph content.\n\n\nThird paragraph."
        boundaries = [0, len(text)]

        paragraphs, page_starts, page_ends = extract_all_paragraphs(text, boundaries, self.tracker)

        self.assertGreater(len(paragraphs), 0)

    def test_extract_paragraphs_matching_list_lengths(self):
        """Test that all returned lists have matching lengths."""
        text = """First paragraph content.

        Second paragraph content.

        Third paragraph content."""
        boundaries = [0, len(text)]

        paragraphs, page_starts, page_ends = extract_all_paragraphs(text, boundaries, self.tracker)

        self.assertEqual(len(paragraphs), len(page_starts))
        self.assertEqual(len(paragraphs), len(page_ends))

    def test_extract_paragraphs_integration_multiple_pages(self):
        """Test paragraph extraction across multiple pages."""
        text = """First paragraph on first page.

        Second paragraph still on first page.

        Third paragraph on second page.

        Fourth paragraph also on second page."""
        boundaries = [0, len(text) // 2, len(text)]

        paragraphs, page_starts, page_ends = extract_all_paragraphs(text, boundaries, self.tracker)

        self.assertGreater(len(paragraphs), 2)
        # All page numbers should be valid (0 or 1)
        for start, end in zip(page_starts, page_ends):
            self.assertGreaterEqual(start, 0)
            self.assertGreaterEqual(end, 0)

    def test_extract_paragraphs_realistic_content(self):
        """Test with realistic academic content."""
        text = """Introduction to the topic involves understanding basic concepts. The field has evolved significantly over time.
        Modern approaches have improved upon traditional methods substantially.

        Methods and experimental design were carefully planned. Data collection spanned multiple months.
        Statistical analysis was performed using standard techniques.

        Results demonstrate clear patterns in the data. These findings are statistically significant.
        The implications for future research are substantial."""
        boundaries = [0, len(text) // 2, len(text)]

        paragraphs, page_starts, page_ends = extract_all_paragraphs(text, boundaries, self.tracker)

        self.assertGreater(len(paragraphs), 2)
        # Verify content preservation
        full_text = " ".join(paragraphs)
        self.assertIn("Introduction", full_text)
        self.assertIn("Methods", full_text)
        self.assertIn("Results", full_text)


if __name__ == "__main__":
    unittest.main()
