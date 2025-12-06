"""Tests for extract_sentences module."""

import sys
import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add pdftools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdftools.extract_sentences import extract_sentences
from pdftools.discard_tracker import DiscardTracker, DiscardType


class TestExtractSentences(unittest.TestCase):
    """Test cases for extract_sentences function."""

    def setUp(self):
        """Set up test fixtures."""
        self.tracker = DiscardTracker()

    def test_extract_sentences_basic(self):
        """Test basic sentence extraction."""
        text = "This is a test sentence. This is another test sentence."
        boundaries = [0, len(text)]

        sentences, page_starts, page_ends = extract_sentences(text, boundaries, self.tracker)

        self.assertEqual(len(sentences), 2)
        self.assertIn("This is a test sentence", sentences[0])
        self.assertIn("This is another test sentence", sentences[1])

    def test_extract_sentences_multiple_pages(self):
        """Test extraction with multiple page boundaries."""
        text = "First sentence. Second sentence. Third sentence."
        # Page boundaries: [0, 20, 40, 50]
        boundaries = [0, 20, 40, len(text)]

        sentences, page_starts, page_ends = extract_sentences(text, boundaries, self.tracker)

        self.assertEqual(len(sentences), 3)
        self.assertEqual(len(page_starts), 3)
        self.assertEqual(len(page_ends), 3)

    def test_extract_sentences_filters_short_sentences(self):
        """Test that sentences shorter than 10 chars are filtered."""
        text = "This is long. Short. This is longer than ten chars."
        boundaries = [0, len(text)]

        sentences, page_starts, page_ends = extract_sentences(text, boundaries, self.tracker)

        # Short sentences should be filtered out
        for sentence in sentences:
            self.assertGreaterEqual(len(sentence), 10)

    def test_extract_sentences_filters_number_only(self):
        """Test that number-only sentences are filtered."""
        text = "This is text. 123. More text here."
        boundaries = [0, len(text)]

        sentences, page_starts, page_ends = extract_sentences(text, boundaries, self.tracker)

        # No sentence should be just a number
        for sentence in sentences:
            self.assertFalse(sentence.isdigit())

    def test_extract_sentences_handles_empty_text(self):
        """Test extraction from empty text."""
        text = ""
        boundaries = [0]

        sentences, page_starts, page_ends = extract_sentences(text, boundaries, self.tracker)

        self.assertEqual(len(sentences), 0)
        self.assertEqual(len(page_starts), 0)
        self.assertEqual(len(page_ends), 0)

    def test_extract_sentences_handles_single_sentence(self):
        """Test extraction with single sentence."""
        text = "This is a single sentence with enough characters."
        boundaries = [0, len(text)]

        sentences, page_starts, page_ends = extract_sentences(text, boundaries, self.tracker)

        self.assertEqual(len(sentences), 1)
        self.assertEqual(len(page_starts), 1)
        self.assertEqual(len(page_ends), 1)

    def test_extract_sentences_various_punctuation(self):
        """Test extraction with different sentence terminators."""
        text = "First sentence. Second question? Third exclamation!"
        boundaries = [0, len(text)]

        sentences, page_starts, page_ends = extract_sentences(text, boundaries, self.tracker)

        self.assertGreaterEqual(len(sentences), 2)

    def test_extract_sentences_preserves_text_content(self):
        """Test that extracted sentences preserve text content."""
        text = "Important information here. Critical data point. Key insight."
        boundaries = [0, len(text)]

        sentences, page_starts, page_ends = extract_sentences(text, boundaries, self.tracker)

        # Verify content is preserved
        extracted_text = " ".join(sentences)
        self.assertIn("Important", extracted_text)
        self.assertIn("Critical", extracted_text)
        self.assertIn("Key", extracted_text)

    def test_extract_sentences_updates_tracker(self):
        """Test that tracker is updated with final character count."""
        text = "This is a test sentence. This is another."
        boundaries = [0, len(text)]

        sentences, _, _ = extract_sentences(text, boundaries, self.tracker)

        # Check that final_character_count is set
        self.assertGreater(self.tracker.final_character_count, 0)
        self.assertEqual(
            self.tracker.final_character_count,
            sum(len(s) for s in sentences)
        )

    def test_extract_sentences_page_positions_ordered(self):
        """Test that page positions are consistent."""
        text = "First long sentence with enough characters. Second sentence also long. Third one."
        boundaries = [0, 30, 60, len(text)]

        sentences, page_starts, page_ends = extract_sentences(text, boundaries, self.tracker)

        # For each sentence, start page should be <= end page
        for start, end in zip(page_starts, page_ends):
            self.assertLessEqual(start, end)

    def test_extract_sentences_whitespace_handling(self):
        """Test that whitespace is properly handled."""
        text = "First sentence.   \n\n   Second sentence."
        boundaries = [0, len(text)]

        sentences, page_starts, page_ends = extract_sentences(text, boundaries, self.tracker)

        # Sentences should be stripped of whitespace
        for sentence in sentences:
            self.assertEqual(sentence, sentence.strip())

    def test_extract_sentences_with_abbreviations(self):
        """Test extraction handles abbreviations with periods."""
        text = "Dr. Smith is here. Prof. Jones arrives. This is another sentence."
        boundaries = [0, len(text)]

        sentences, page_starts, page_ends = extract_sentences(text, boundaries, self.tracker)

        # Should handle abbreviations reasonably
        self.assertGreater(len(sentences), 0)

    def test_extract_sentences_tracks_short_lines(self):
        """Test that short lines are tracked as discards."""
        text = "This is a real sentence. Very short. Another long sentence here."
        boundaries = [0, len(text)]

        initial_count = len(self.tracker.discards)
        sentences, page_starts, page_ends = extract_sentences(text, boundaries, self.tracker)

        # Should have recorded some discards for short sentences
        new_discards = len(self.tracker.discards) - initial_count
        self.assertGreater(new_discards, 0)

    def test_extract_sentences_returns_tuple(self):
        """Test that function returns a tuple of three lists."""
        text = "First sentence. Second sentence."
        boundaries = [0, len(text)]

        result = extract_sentences(text, boundaries, self.tracker)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)
        self.assertIsInstance(result[0], list)  # sentences
        self.assertIsInstance(result[1], list)  # page_starts
        self.assertIsInstance(result[2], list)  # page_ends

    def test_extract_sentences_matching_list_lengths(self):
        """Test that returned lists have matching lengths."""
        text = "Sentence one here. Sentence two here. Sentence three here."
        boundaries = [0, len(text)]

        sentences, page_starts, page_ends = extract_sentences(text, boundaries, self.tracker)

        self.assertEqual(len(sentences), len(page_starts))
        self.assertEqual(len(sentences), len(page_ends))

    def test_extract_sentences_integration_with_tracker(self):
        """Test integration with DiscardTracker."""
        text = "Valid sentence. Bad. Good sentence again."
        boundaries = [0, len(text)]

        sentences, _, _ = extract_sentences(text, boundaries, self.tracker)

        # Tracker should have recorded discards
        stats = self.tracker.get_statistics()
        self.assertIn("total_items_discarded", stats)

    def test_extract_sentences_unicode_handling(self):
        """Test extraction with unicode characters."""
        text = "Français is here. Español también. English too."
        boundaries = [0, len(text)]

        sentences, page_starts, page_ends = extract_sentences(text, boundaries, self.tracker)

        self.assertGreater(len(sentences), 0)
        # Check unicode is preserved
        extracted = " ".join(sentences)
        self.assertIn("Français", extracted)

    def test_extract_sentences_complex_text(self):
        """Test with more complex, realistic text."""
        text = """Advanced techniques are described. Machine learning models work well.
        Deep neural networks have proven effective. However, they require significant computational resources.
        This is a comprehensive study. The results show promise."""
        boundaries = [0, len(text) // 2, len(text)]

        sentences, page_starts, page_ends = extract_sentences(text, boundaries, self.tracker)

        self.assertGreater(len(sentences), 3)
        self.assertEqual(len(sentences), len(page_starts))
        self.assertEqual(len(sentences), len(page_ends))


if __name__ == "__main__":
    unittest.main()
