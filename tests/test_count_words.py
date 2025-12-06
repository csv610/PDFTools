"""Tests for the count_words module."""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile

# Add pdftools to path
sys.path.insert(0, str(Path(__file__).parent.parent / "pdftools"))

from count_words import count_words_in_pdf


class TestCountWordsInPdf:
    """Tests for count_words_in_pdf function."""

    def test_count_words_single_page(self, tmp_path):
        """Test counting words on a single page PDF."""
        mock_page = Mock()
        mock_page.extract_text.return_value = "This is a simple test"

        mock_reader = Mock()
        mock_reader.pages = [mock_page]

        # Create a temporary PDF file
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"dummy pdf content")

        with patch('count_words.PdfReader', return_value=mock_reader):
            result = count_words_in_pdf(str(pdf_file))

        assert result is not None
        assert result['total_words'] == 5  # "This", "is", "a", "simple", "test"
        assert result['pages_processed'] == 1
        assert result['start_page'] == 1
        assert result['end_page'] == 1
        assert result['total_pages'] == 1

    def test_count_words_multiple_pages(self, tmp_path):
        """Test counting words across multiple pages."""
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "Page one text"

        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "Page two text"

        mock_page3 = Mock()
        mock_page3.extract_text.return_value = "Page three content"

        mock_reader = Mock()
        mock_reader.pages = [mock_page1, mock_page2, mock_page3]

        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"dummy pdf content")

        with patch('count_words.PdfReader', return_value=mock_reader):
            result = count_words_in_pdf(str(pdf_file))

        assert result['total_pages'] == 3
        assert result['total_words'] == 9  # "Page" "one" "text" "Page" "two" "text" "Page" "three" "content"
        assert result['pages_processed'] == 3

    def test_count_words_with_page_range(self, tmp_path):
        """Test counting words with specific page range."""
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "First page"

        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "Second page"

        mock_page3 = Mock()
        mock_page3.extract_text.return_value = "Third page"

        mock_reader = Mock()
        mock_reader.pages = [mock_page1, mock_page2, mock_page3]

        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"dummy pdf content")

        with patch('count_words.PdfReader', return_value=mock_reader):
            # Count only pages 2-3
            result = count_words_in_pdf(str(pdf_file), start_page=2, end_page=3)

        assert result['start_page'] == 2
        assert result['end_page'] == 3
        assert result['pages_processed'] == 2
        assert result['total_words'] == 4  # "Second", "page", "Third", "page"

    def test_count_words_single_page_in_range(self, tmp_path):
        """Test counting words from a single page within range."""
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "First page"

        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "Second page"

        mock_page3 = Mock()
        mock_page3.extract_text.return_value = "Third page"

        mock_reader = Mock()
        mock_reader.pages = [mock_page1, mock_page2, mock_page3]

        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"dummy pdf content")

        with patch('count_words.PdfReader', return_value=mock_reader):
            result = count_words_in_pdf(str(pdf_file), start_page=2, end_page=2)

        assert result['start_page'] == 2
        assert result['end_page'] == 2
        assert result['pages_processed'] == 1
        assert result['total_words'] == 2  # "Second", "page"

    def test_count_words_empty_page(self, tmp_path):
        """Test handling of empty pages."""
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "Content here"

        mock_page2 = Mock()
        mock_page2.extract_text.return_value = ""  # Empty page

        mock_page3 = Mock()
        mock_page3.extract_text.return_value = "More content"

        mock_reader = Mock()
        mock_reader.pages = [mock_page1, mock_page2, mock_page3]

        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"dummy pdf content")

        with patch('count_words.PdfReader', return_value=mock_reader):
            result = count_words_in_pdf(str(pdf_file))

        # Should skip empty page
        assert result['pages_processed'] == 2
        assert result['total_words'] == 4  # "Content", "here", "More", "content"

    def test_count_words_none_page(self, tmp_path):
        """Test handling of pages that return None."""
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "Content"

        mock_page2 = Mock()
        mock_page2.extract_text.return_value = None  # No text extraction

        mock_page3 = Mock()
        mock_page3.extract_text.return_value = "More"

        mock_reader = Mock()
        mock_reader.pages = [mock_page1, mock_page2, mock_page3]

        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"dummy pdf content")

        with patch('count_words.PdfReader', return_value=mock_reader):
            result = count_words_in_pdf(str(pdf_file))

        assert result['pages_processed'] == 2
        assert result['total_words'] == 2

    def test_count_words_with_punctuation(self, tmp_path):
        """Test word counting with punctuation."""
        mock_page = Mock()
        mock_page.extract_text.return_value = "Hello, world! How are you?"

        mock_reader = Mock()
        mock_reader.pages = [mock_page]

        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"dummy pdf content")

        with patch('count_words.PdfReader', return_value=mock_reader):
            result = count_words_in_pdf(str(pdf_file))

        # Should count 5 words (punctuation doesn't split words)
        assert result['total_words'] == 5

    def test_count_words_with_hyphens(self, tmp_path):
        """Test word counting handles hyphenated words correctly."""
        mock_page = Mock()
        mock_page.extract_text.return_value = "well-known state-of-the-art method"

        mock_reader = Mock()
        mock_reader.pages = [mock_page]

        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"dummy pdf content")

        with patch('count_words.PdfReader', return_value=mock_reader):
            result = count_words_in_pdf(str(pdf_file))

        # Split on hyphens: "well", "known", "state", "of", "the", "art", "method"
        assert result['total_words'] == 7

    def test_count_words_with_multiple_spaces(self, tmp_path):
        """Test word counting with multiple whitespaces."""
        mock_page = Mock()
        mock_page.extract_text.return_value = "word1   word2     word3"

        mock_reader = Mock()
        mock_reader.pages = [mock_page]

        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"dummy pdf content")

        with patch('count_words.PdfReader', return_value=mock_reader):
            result = count_words_in_pdf(str(pdf_file))

        assert result['total_words'] == 3

    def test_count_words_file_not_found(self):
        """Test error when PDF file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            count_words_in_pdf("/nonexistent/path/file.pdf")

    def test_count_words_not_pdf_file(self, tmp_path):
        """Test error when file is not a PDF."""
        text_file = tmp_path / "not_a_pdf.txt"
        text_file.write_text("This is not a PDF")

        with pytest.raises(ValueError, match="is not a PDF file"):
            count_words_in_pdf(str(text_file))

    def test_count_words_invalid_start_page(self, tmp_path):
        """Test error when start_page is less than 1."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"dummy pdf content")

        with pytest.raises(ValueError, match="start_page must be at least 1"):
            count_words_in_pdf(str(pdf_file), start_page=0)

    def test_count_words_start_page_exceeds_total(self, tmp_path):
        """Test error when start_page exceeds total pages."""
        mock_reader = Mock()
        mock_reader.pages = [Mock(), Mock()]  # 2 pages

        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"dummy pdf content")

        with patch('count_words.PdfReader', return_value=mock_reader):
            with pytest.raises((ValueError, RuntimeError)):
                count_words_in_pdf(str(pdf_file), start_page=5)

    def test_count_words_end_page_before_start(self, tmp_path):
        """Test error when end_page is before start_page."""
        mock_reader = Mock()
        mock_reader.pages = [Mock(), Mock(), Mock()]  # 3 pages

        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"dummy pdf content")

        with patch('count_words.PdfReader', return_value=mock_reader):
            with pytest.raises((ValueError, RuntimeError)):
                count_words_in_pdf(str(pdf_file), start_page=3, end_page=1)

    def test_count_words_end_page_exceeds_total(self, tmp_path):
        """Test error when end_page exceeds total pages."""
        mock_reader = Mock()
        mock_reader.pages = [Mock(), Mock()]  # 2 pages

        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"dummy pdf content")

        with patch('count_words.PdfReader', return_value=mock_reader):
            with pytest.raises((ValueError, RuntimeError)):
                count_words_in_pdf(str(pdf_file), end_page=5)

    def test_count_words_empty_pdf(self, tmp_path):
        """Test error when PDF has no pages."""
        mock_reader = Mock()
        mock_reader.pages = []

        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"dummy pdf content")

        with patch('count_words.PdfReader', return_value=mock_reader):
            with pytest.raises((ValueError, RuntimeError)):
                count_words_in_pdf(str(pdf_file))

    def test_count_words_extraction_exception(self, tmp_path):
        """Test handling of extraction exceptions on a page."""
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "First page"

        mock_page2 = Mock()
        mock_page2.extract_text.side_effect = Exception("Extraction error")

        mock_page3 = Mock()
        mock_page3.extract_text.return_value = "Third page"

        mock_reader = Mock()
        mock_reader.pages = [mock_page1, mock_page2, mock_page3]

        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"dummy pdf content")

        with patch('count_words.PdfReader', return_value=mock_reader):
            # Should continue despite page 2 error
            result = count_words_in_pdf(str(pdf_file))

        # Should process pages 1 and 3 (page 2 failed)
        assert result['pages_processed'] == 2
        assert result['total_words'] == 4

    def test_count_words_complex_text(self, tmp_path):
        """Test word counting with complex text."""
        mock_page = Mock()
        mock_page.extract_text.return_value = (
            "Machine learning is a subset of artificial intelligence.\n"
            "It focuses on algorithms and data-driven approaches."
        )

        mock_reader = Mock()
        mock_reader.pages = [mock_page]

        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"dummy pdf content")

        with patch('count_words.PdfReader', return_value=mock_reader):
            result = count_words_in_pdf(str(pdf_file))

        # Count: Machine, learning, is, a, subset, of, artificial, intelligence (8)
        # + It, focuses, on, algorithms, and, data (6), driven, approaches (2) = 16 words
        assert result['total_words'] == 16
        assert result['pages_processed'] == 1

    def test_count_words_returns_dict(self, tmp_path):
        """Test that the function returns a proper dictionary."""
        mock_page = Mock()
        mock_page.extract_text.return_value = "test content"

        mock_reader = Mock()
        mock_reader.pages = [mock_page]

        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"dummy pdf content")

        with patch('count_words.PdfReader', return_value=mock_reader):
            result = count_words_in_pdf(str(pdf_file))

        # Verify all expected keys are present
        assert 'total_words' in result
        assert 'pages_processed' in result
        assert 'start_page' in result
        assert 'end_page' in result
        assert 'total_pages' in result

    def test_count_words_integration_multiple_ranges(self, tmp_path):
        """Test multiple calls with different page ranges."""
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "Page one"

        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "Page two"

        mock_page3 = Mock()
        mock_page3.extract_text.return_value = "Page three"

        mock_reader = Mock()
        mock_reader.pages = [mock_page1, mock_page2, mock_page3]

        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"dummy pdf content")

        with patch('count_words.PdfReader', return_value=mock_reader):
            # Count all pages
            all_result = count_words_in_pdf(str(pdf_file))
            assert all_result['total_words'] == 6

            # Count first page only
            first_result = count_words_in_pdf(str(pdf_file), start_page=1, end_page=1)
            assert first_result['total_words'] == 2

            # Count last two pages
            last_result = count_words_in_pdf(str(pdf_file), start_page=2, end_page=3)
            assert last_result['total_words'] == 4
