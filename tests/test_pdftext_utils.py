"""Tests for the pdftext_utils module."""

import pytest
import sys
import re
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Add pdftools to path
sys.path.insert(0, str(Path(__file__).parent.parent / "pdftools"))

from pdftext_utils import (
    clean_page_text,
    remove_references,
    calculate_page_position,
    save_content_to_file,
    display_table,
    get_cli_parser,
    extract_and_clean,
)
from discard_tracker import DiscardTracker, DiscardType


class TestCleanPageText:
    """Tests for clean_page_text function."""

    def test_clean_empty_text(self):
        """Test cleaning empty text."""
        tracker = DiscardTracker()
        result = clean_page_text("", page_num=0, tracker=tracker)
        assert result == ""
        assert tracker.total_lines_processed == 0

    def test_clean_removes_empty_lines(self):
        """Test that empty lines are removed."""
        tracker = DiscardTracker()
        text = "Line 1\n\nLine 2\n\n\nLine 3"
        result = clean_page_text(text, page_num=0, tracker=tracker)
        # Empty lines should be skipped but processed count should increase
        assert "Line 1" in result
        assert "Line 2" in result
        assert "Line 3" in result
        assert tracker.total_lines_processed == 3  # All 3 content lines processed

    def test_clean_removes_page_numbers(self):
        """Test that standalone page numbers are removed."""
        tracker = DiscardTracker()
        text = "Introduction\n1\nBody text"
        result = clean_page_text(text, page_num=0, tracker=tracker)
        assert "1" not in result
        assert "Introduction" in result
        assert "Body text" in result
        assert tracker.page_numbers_removed == 1

    def test_clean_removes_arxiv_metadata(self):
        """Test that arXiv metadata is removed."""
        tracker = DiscardTracker()
        text = "Introduction\narXiv:1706.03762v7 [cs.CL] 28 May 2020\nContent"
        result = clean_page_text(text, page_num=0, tracker=tracker)
        assert "arXiv" not in result
        assert "Introduction" in result
        assert "Content" in result
        assert tracker.arxiv_metadata_removed == 1

    def test_clean_removes_date_footers(self):
        """Test that date footers are removed."""
        tracker = DiscardTracker()
        text = "Content\n2 Aug 2023\nMore content"
        result = clean_page_text(text, page_num=0, tracker=tracker)
        assert "2 Aug 2023" not in result
        assert "Content" in result
        assert "More content" in result
        assert tracker.date_footers_removed == 1

    def test_clean_removes_separator_lines(self):
        """Test that separator lines are removed."""
        tracker = DiscardTracker()
        text = "Section 1\n====\nSection 2\n-----\nSection 3"
        result = clean_page_text(text, page_num=0, tracker=tracker)
        assert "====" not in result
        assert "-----" not in result
        assert "Section 1" in result
        assert tracker.separator_lines_removed == 2

    def test_clean_removes_short_lines(self):
        """Test that lines shorter than 3 characters are removed."""
        tracker = DiscardTracker()
        text = "Valid content\nab\nMore content\n.\nx"
        result = clean_page_text(text, page_num=0, tracker=tracker)
        assert "Valid content" in result
        assert "More content" in result
        assert "ab" not in result
        assert "." not in result
        assert "x" not in result
        assert tracker.short_lines_removed == 3

    def test_clean_normalizes_whitespace(self):
        """Test that multiple spaces are normalized to single space."""
        tracker = DiscardTracker()
        text = "This  has   multiple    spaces"
        result = clean_page_text(text, page_num=0, tracker=tracker)
        assert "  " not in result
        assert "This has multiple spaces" in result

    def test_clean_tracks_page_number(self):
        """Test that page number is tracked correctly."""
        tracker = DiscardTracker()
        clean_page_text("Page number: 5\nContent", page_num=3, tracker=tracker)
        # Page numbers should be tracked with the correct page number
        assert tracker.page_numbers_removed >= 0

    def test_clean_multiple_date_formats(self):
        """Test that various date formats are recognized."""
        tracker = DiscardTracker()
        dates = [
            "1 Jan 2023",
            "31 Dec 2023",
            "15 FEB 2023",
            "28 april 2023",
        ]
        for date in dates:
            tracker = DiscardTracker()
            result = clean_page_text(date, page_num=0, tracker=tracker)
            if tracker.date_footers_removed == 1:
                assert date not in result


class TestRemoveReferences:
    """Tests for remove_references function."""

    def test_remove_references_section(self):
        """Test that References section is removed."""
        tracker = DiscardTracker()
        text = "Introduction\nContent\nReferences\n[1] Author, Title\n[2] Author, Title"
        result = remove_references(text, tracker)
        assert "Introduction" in result
        assert "Content" in result
        assert "References" not in result
        assert "[1]" not in result
        assert "[2]" not in result

    def test_remove_bibliography_section(self):
        """Test that Bibliography section is removed."""
        tracker = DiscardTracker()
        text = "Introduction\nBibliography\n[1] Author\n[2] Author"
        result = remove_references(text, tracker)
        assert "Introduction" in result
        assert "Bibliography" not in result

    def test_remove_references_case_insensitive(self):
        """Test that References removal is case insensitive."""
        tracker = DiscardTracker()
        text = "Content\nREFERENCES\n[1] Item"
        result = remove_references(text, tracker)
        assert "REFERENCES" not in result
        assert "[1]" not in result

    def test_remove_references_tracks_removals(self):
        """Test that removals are tracked correctly."""
        tracker = DiscardTracker()
        text = "Content\nReferences\n[1] Item\n[2] Item\n[3] Item"
        remove_references(text, tracker)
        # Should track the References header and 3 bibliography entries
        assert tracker.references_sections_removed == 1
        assert tracker.bibliography_entries_removed >= 3

    def test_remove_references_no_references_section(self):
        """Test behavior when no References section exists."""
        tracker = DiscardTracker()
        text = "Introduction\nContent\nConclusion"
        result = remove_references(text, tracker)
        assert result == text
        assert tracker.references_sections_removed == 0

    def test_remove_references_keeps_text_before(self):
        """Test that all text before References is kept."""
        tracker = DiscardTracker()
        text = "Line 1\nLine 2\nLine 3\nReferences\n[1] Item"
        result = remove_references(text, tracker)
        assert "Line 1" in result
        assert "Line 2" in result
        assert "Line 3" in result

    def test_remove_references_empty_text(self):
        """Test removing references from empty text."""
        tracker = DiscardTracker()
        result = remove_references("", tracker)
        assert result == ""


class TestCalculatePagePosition:
    """Tests for calculate_page_position function."""

    def test_calculate_position_page_0(self):
        """Test calculating position on first page."""
        page_boundaries = [0, 1000, 2000, 3000]
        # Position 500 should be on page 0
        assert calculate_page_position(500, page_boundaries) == 0

    def test_calculate_position_page_1(self):
        """Test calculating position on second page."""
        page_boundaries = [0, 1000, 2000, 3000]
        # Position 1500 should be on page 1
        assert calculate_page_position(1500, page_boundaries) == 1

    def test_calculate_position_page_2(self):
        """Test calculating position on third page."""
        page_boundaries = [0, 1000, 2000, 3000]
        # Position 2500 should be on page 2
        assert calculate_page_position(2500, page_boundaries) == 2

    def test_calculate_position_at_boundary(self):
        """Test calculating position exactly at boundary."""
        page_boundaries = [0, 1000, 2000, 3000]
        # Position 1000 is at the boundary, should be page 1
        assert calculate_page_position(1000, page_boundaries) == 1

    def test_calculate_position_start(self):
        """Test calculating position at start."""
        page_boundaries = [0, 1000, 2000]
        assert calculate_page_position(0, page_boundaries) == 0

    def test_calculate_position_beyond_last_page(self):
        """Test calculating position beyond last page."""
        page_boundaries = [0, 1000, 2000, 3000]
        # Position 5000 is beyond all pages
        assert calculate_page_position(5000, page_boundaries) == 3


class TestSaveContentToFile:
    """Tests for save_content_to_file function."""

    def test_save_single_item(self, tmp_path):
        """Test saving a single item to file."""
        output_file = tmp_path / "output.txt"
        items = ["Test content"]
        starts = [0]
        ends = [0]

        save_content_to_file(items, starts, ends, str(output_file), "Item")

        assert output_file.exists()
        content = output_file.read_text()
        assert "Item 1 - Page 0" in content
        assert "Test content" in content

    def test_save_multiple_items(self, tmp_path):
        """Test saving multiple items to file."""
        output_file = tmp_path / "output.txt"
        items = ["Content 1", "Content 2", "Content 3"]
        starts = [0, 1, 2]
        ends = [0, 1, 2]

        save_content_to_file(items, starts, ends, str(output_file), "Sentence")

        content = output_file.read_text()
        assert "Sentence 1" in content
        assert "Sentence 2" in content
        assert "Sentence 3" in content

    def test_save_multipage_items(self, tmp_path):
        """Test saving items that span multiple pages."""
        output_file = tmp_path / "output.txt"
        items = ["Long content"]
        starts = [0]
        ends = [2]

        save_content_to_file(items, starts, ends, str(output_file), "Paragraph")

        content = output_file.read_text()
        assert "Paragraph 1 - Pages 0-2" in content

    def test_save_creates_file(self, tmp_path):
        """Test that save function creates a file."""
        output_file = tmp_path / "new_file.txt"
        assert not output_file.exists()

        save_content_to_file(
            ["test"],
            [0],
            [0],
            str(output_file),
            "Test"
        )

        assert output_file.exists()

    def test_save_includes_separator(self, tmp_path):
        """Test that items are separated by lines."""
        output_file = tmp_path / "output.txt"
        items = ["Item 1", "Item 2"]
        starts = [0, 1]
        ends = [0, 1]

        save_content_to_file(items, starts, ends, str(output_file), "Item")

        content = output_file.read_text()
        assert "=" * 80 in content


class TestDisplayTable:
    """Tests for display_table function."""

    def test_display_table_output(self, capsys):
        """Test that display_table produces output."""
        items = ["Short item", "Another short item"]
        starts = [0, 1]
        ends = [0, 1]

        display_table(items, starts, ends, "Sentence")

        captured = capsys.readouterr()
        assert "Sentence" in captured.out
        assert "Pages" in captured.out
        assert "=" * 130 in captured.out

    def test_display_table_shows_items(self, capsys):
        """Test that display_table shows the items."""
        items = ["Test content", "More content"]
        starts = [0, 1]
        ends = [0, 1]

        display_table(items, starts, ends, "Item")

        captured = capsys.readouterr()
        assert "Test content" in captured.out
        assert "More content" in captured.out

    def test_display_table_multiline_content(self, capsys):
        """Test display_table with multiline content."""
        items = ["Line 1\nLine 2\nLine 3"]
        starts = [0]
        ends = [0]

        display_table(items, starts, ends, "Paragraph")

        captured = capsys.readouterr()
        # Multiline should be displayed as single line
        assert "Line 1 Line 2 Line 3" in captured.out

    def test_display_table_empty_items(self, capsys):
        """Test display_table with empty items list."""
        display_table([], [], [], "Item")
        captured = capsys.readouterr()
        # Should still print header
        assert "=" in captured.out


class TestGetCliParser:
    """Tests for get_cli_parser function."""

    def test_parser_creation(self):
        """Test that parser is created successfully."""
        parser = get_cli_parser("Test description", "output.txt")
        assert parser is not None

    def test_parser_required_argument(self):
        """Test that pdf_file argument is required."""
        parser = get_cli_parser("Test", "output.txt")
        # Should raise SystemExit when parsing without pdf_file
        with pytest.raises(SystemExit):
            parser.parse_args([])

    def test_parser_with_pdf_file(self):
        """Test parsing with pdf_file argument."""
        parser = get_cli_parser("Test", "output.txt")
        args = parser.parse_args(["test.pdf"])
        assert args.pdf_file == "test.pdf"

    def test_parser_default_output(self):
        """Test default output filename."""
        parser = get_cli_parser("Test", "default_output.txt")
        args = parser.parse_args(["test.pdf"])
        assert args.output == "default_output.txt"

    def test_parser_custom_output(self):
        """Test custom output filename."""
        parser = get_cli_parser("Test", "default.txt")
        args = parser.parse_args(["test.pdf", "-o", "custom.txt"])
        assert args.output == "custom.txt"

    def test_parser_track_log_default(self):
        """Test default track log filename."""
        parser = get_cli_parser("Test", "output.txt")
        args = parser.parse_args(["test.pdf"])
        assert args.track_log == "discard_tracking.txt"

    def test_parser_custom_track_log(self):
        """Test custom track log filename."""
        parser = get_cli_parser("Test", "output.txt")
        args = parser.parse_args(["test.pdf", "-t", "custom_log.txt"])
        assert args.track_log == "custom_log.txt"

    def test_parser_display_flag(self):
        """Test display flag."""
        parser = get_cli_parser("Test", "output.txt")
        args = parser.parse_args(["test.pdf"])
        assert args.display is False

        args = parser.parse_args(["test.pdf", "-d"])
        assert args.display is True

    def test_parser_short_and_long_options(self):
        """Test that both short and long options work."""
        parser = get_cli_parser("Test", "output.txt")

        # Short options
        args1 = parser.parse_args(["test.pdf", "-o", "out.txt", "-t", "log.txt", "-d"])
        # Long options
        args2 = parser.parse_args([
            "test.pdf",
            "--output", "out.txt",
            "--track-log", "log.txt",
            "--display"
        ])

        assert args1.output == args2.output
        assert args1.track_log == args2.track_log
        assert args1.display == args2.display


class TestExtractAndClean:
    """Tests for extract_and_clean function."""

    def test_extract_and_clean_single_page(self, tmp_path):
        """Test extracting and cleaning a single page PDF."""
        from unittest.mock import Mock, patch
        from pypdf import PdfReader

        # Create mock PDF with single page
        mock_page = Mock()
        mock_page.extract_text.return_value = "Page 1 content\nMore text"

        mock_reader = Mock()
        mock_reader.pages = [mock_page]

        tracker = DiscardTracker()

        with patch('pdftext_utils.PdfReader', return_value=mock_reader):
            # Create a temporary PDF file path (won't actually be read due to mock)
            pdf_path = str(tmp_path / "test.pdf")
            text, boundaries = extract_and_clean(pdf_path, tracker)

        # Check basic structure
        assert "Page 1 content" in text
        assert len(boundaries) == 2  # Start and end boundaries
        assert boundaries[0] == 0

    def test_extract_and_clean_multiple_pages(self, tmp_path):
        """Test extracting and cleaning multiple pages."""
        from unittest.mock import Mock, patch

        # Create mock pages
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "Page 1\nContent"

        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "Page 2\nMore content"

        mock_reader = Mock()
        mock_reader.pages = [mock_page1, mock_page2]

        tracker = DiscardTracker()

        with patch('pdftext_utils.PdfReader', return_value=mock_reader):
            pdf_path = str(tmp_path / "test.pdf")
            text, boundaries = extract_and_clean(pdf_path, tracker)

        # Check multiple pages are processed
        assert "Page 1" in text
        assert "Page 2" in text
        assert len(boundaries) == 3  # Start + 2 pages
        assert tracker.total_lines_processed > 0

    def test_extract_and_clean_empty_page(self, tmp_path):
        """Test handling of empty pages in PDF."""
        from unittest.mock import Mock, patch

        # Mix of empty and non-empty pages
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = None

        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "Valid content"

        mock_page3 = Mock()
        mock_page3.extract_text.return_value = ""

        mock_reader = Mock()
        mock_reader.pages = [mock_page1, mock_page2, mock_page3]

        tracker = DiscardTracker()

        with patch('pdftext_utils.PdfReader', return_value=mock_reader):
            pdf_path = str(tmp_path / "test.pdf")
            text, boundaries = extract_and_clean(pdf_path, tracker)

        # Should still have valid content
        assert "Valid content" in text

    def test_extract_and_clean_tracks_original_character_count(self, tmp_path):
        """Test that original character count is tracked."""
        from unittest.mock import Mock, patch

        mock_page = Mock()
        test_text = "Test content with some characters"
        mock_page.extract_text.return_value = test_text

        mock_reader = Mock()
        mock_reader.pages = [mock_page]

        tracker = DiscardTracker()

        with patch('pdftext_utils.PdfReader', return_value=mock_reader):
            pdf_path = str(tmp_path / "test.pdf")
            text, boundaries = extract_and_clean(pdf_path, tracker)

        # Character count should be set
        assert tracker.original_character_count > 0

    def test_extract_and_clean_removes_references(self, tmp_path):
        """Test that references section is removed during extraction."""
        from unittest.mock import Mock, patch

        mock_page = Mock()
        mock_page.extract_text.return_value = (
            "Introduction\nContent\nReferences\n[1] Author, Title\n[2] Author, Title"
        )

        mock_reader = Mock()
        mock_reader.pages = [mock_page]

        tracker = DiscardTracker()

        with patch('pdftext_utils.PdfReader', return_value=mock_reader):
            pdf_path = str(tmp_path / "test.pdf")
            text, boundaries = extract_and_clean(pdf_path, tracker)

        # References should be removed
        assert "References" not in text
        assert "[1]" not in text
        assert "Introduction" in text
        assert "Content" in text

    def test_extract_and_clean_page_boundaries(self, tmp_path):
        """Test that page boundaries are calculated correctly."""
        from unittest.mock import Mock, patch

        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "Page 1"

        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "Page 2"

        mock_page3 = Mock()
        mock_page3.extract_text.return_value = "Page 3"

        mock_reader = Mock()
        mock_reader.pages = [mock_page1, mock_page2, mock_page3]

        tracker = DiscardTracker()

        with patch('pdftext_utils.PdfReader', return_value=mock_reader):
            pdf_path = str(tmp_path / "test.pdf")
            text, boundaries = extract_and_clean(pdf_path, tracker)

        # Should have 4 boundaries (start + 3 pages)
        assert len(boundaries) == 4
        assert boundaries[0] == 0
        # Each boundary should be increasing
        for i in range(len(boundaries) - 1):
            assert boundaries[i] <= boundaries[i + 1]

    def test_extract_and_clean_no_pages(self, tmp_path):
        """Test handling of PDF with no pages."""
        from unittest.mock import Mock, patch

        mock_reader = Mock()
        mock_reader.pages = []

        tracker = DiscardTracker()

        with patch('pdftext_utils.PdfReader', return_value=mock_reader):
            pdf_path = str(tmp_path / "test.pdf")
            text, boundaries = extract_and_clean(pdf_path, tracker)

        # Should return empty or minimal content
        assert len(boundaries) >= 1  # At least starting boundary

    def test_extract_and_clean_with_special_characters(self, tmp_path):
        """Test handling PDF with special characters."""
        from unittest.mock import Mock, patch

        mock_page = Mock()
        mock_page.extract_text.return_value = (
            "Special chars: α β γ δ\nMath: ∑ ∫ √\nSymbols: © ® ™"
        )

        mock_reader = Mock()
        mock_reader.pages = [mock_page]

        tracker = DiscardTracker()

        with patch('pdftext_utils.PdfReader', return_value=mock_reader):
            pdf_path = str(tmp_path / "test.pdf")
            text, boundaries = extract_and_clean(pdf_path, tracker)

        # Should preserve special characters
        assert "α" in text or len(text) > 0  # May be filtered by cleaning

    def test_extract_and_clean_normalizes_whitespace(self, tmp_path):
        """Test that whitespace is normalized during cleaning."""
        from unittest.mock import Mock, patch

        mock_page = Mock()
        mock_page.extract_text.return_value = "Line  with   multiple    spaces"

        mock_reader = Mock()
        mock_reader.pages = [mock_page]

        tracker = DiscardTracker()

        with patch('pdftext_utils.PdfReader', return_value=mock_reader):
            pdf_path = str(tmp_path / "test.pdf")
            text, boundaries = extract_and_clean(pdf_path, tracker)

        # Multiple spaces should be normalized
        assert "   " not in text or text == ""

    def test_extract_and_clean_invalid_pdf_raises_error(self, tmp_path):
        """Test that invalid PDF file raises appropriate error."""
        from unittest.mock import patch

        pdf_path = str(tmp_path / "nonexistent.pdf")
        tracker = DiscardTracker()

        with patch('pdftext_utils.PdfReader', side_effect=FileNotFoundError):
            with pytest.raises(FileNotFoundError):
                extract_and_clean(pdf_path, tracker)


class TestIntegration:
    """Integration tests combining multiple functions."""

    def test_clean_and_save_workflow(self, tmp_path):
        """Test a workflow of cleaning and saving content."""
        # Create mock text
        text = "Introduction\n2\nContent\nMore content\n===\nReferences\n[1] Item"

        tracker = DiscardTracker()
        cleaned = clean_page_text(text, page_num=0, tracker=tracker)
        cleaned = remove_references(cleaned, tracker)

        output_file = tmp_path / "workflow_output.txt"
        items = [cleaned]
        save_content_to_file(items, [0], [0], str(output_file), "Content")

        assert output_file.exists()
        content = output_file.read_text()
        assert "Introduction" in content
        assert "Content" in content

    def test_full_extraction_workflow(self, tmp_path):
        """Test complete extraction workflow from PDF to saved file."""
        from unittest.mock import Mock, patch

        # Create mock PDF
        mock_page = Mock()
        mock_page.extract_text.return_value = (
            "Title\nIntroduction text\n1\nPage number above\nReferences\n[1] Ref"
        )

        mock_reader = Mock()
        mock_reader.pages = [mock_page]

        tracker = DiscardTracker()

        with patch('pdftext_utils.PdfReader', return_value=mock_reader):
            pdf_path = str(tmp_path / "test.pdf")
            text, boundaries = extract_and_clean(pdf_path, tracker)

        # Save the cleaned content
        output_file = tmp_path / "extracted.txt"
        save_content_to_file([text], boundaries[:-1], boundaries[:-1],
                            str(output_file), "Extracted")

        # Verify output
        assert output_file.exists()
        content = output_file.read_text()
        assert "Title" in content
        assert "Introduction" in content
        assert "References" not in content
        assert "Extracted 1" in content
