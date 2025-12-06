"""Tests for the discard_tracker module."""

import pytest
import sys
from pathlib import Path

# Add pdftools to path
sys.path.insert(0, str(Path(__file__).parent.parent / "pdftools"))

from discard_tracker import DiscardType, DiscardedItem, DiscardTracker


class TestDiscardType:
    """Tests for DiscardType enum."""

    def test_discard_type_values(self):
        """Test that all DiscardType values are defined."""
        assert DiscardType.PAGE_NUMBER.value == "page_number"
        assert DiscardType.HEADER_FOOTER.value == "header_footer"
        assert DiscardType.ARXIV_METADATA.value == "arxiv_metadata"
        assert DiscardType.DATE_FOOTER.value == "date_footer"
        assert DiscardType.SEPARATOR_LINE.value == "separator_line"
        assert DiscardType.SHORT_LINE.value == "short_line"
        assert DiscardType.REFERENCES_SECTION.value == "references_section"
        assert DiscardType.BIBLIOGRAPHY_ENTRY.value == "bibliography_entry"
        assert DiscardType.OTHER.value == "other"


class TestDiscardedItem:
    """Tests for DiscardedItem dataclass."""

    def test_discarded_item_creation(self):
        """Test creating a DiscardedItem."""
        item = DiscardedItem(
            discard_type=DiscardType.PAGE_NUMBER,
            content="1",
            page_number=0,
            line_number=1,
            reason="Standalone page number"
        )
        assert item.discard_type == DiscardType.PAGE_NUMBER
        assert item.content == "1"
        assert item.page_number == 0
        assert item.line_number == 1
        assert item.reason == "Standalone page number"

    def test_discarded_item_defaults(self):
        """Test DiscardedItem with default values."""
        item = DiscardedItem(
            discard_type=DiscardType.OTHER,
            content="some content"
        )
        assert item.page_number == 0
        assert item.line_number == 0
        assert item.reason == ""

    def test_discarded_item_str(self):
        """Test DiscardedItem string representation."""
        item = DiscardedItem(
            discard_type=DiscardType.PAGE_NUMBER,
            content="1",
            page_number=5,
            line_number=10
        )
        str_repr = str(item)
        assert "[page_number]" in str_repr
        assert "Page 5" in str_repr
        assert "Line 10" in str_repr

    def test_discarded_item_long_content_truncated(self):
        """Test that long content is truncated in string representation."""
        long_content = "x" * 100
        item = DiscardedItem(
            discard_type=DiscardType.OTHER,
            content=long_content
        )
        str_repr = str(item)
        assert "..." in str_repr
        assert len(str_repr) < len(long_content)


class TestDiscardTracker:
    """Tests for DiscardTracker class."""

    def test_tracker_initialization(self):
        """Test DiscardTracker initialization."""
        tracker = DiscardTracker()
        assert tracker.page_numbers_removed == 0
        assert tracker.headers_footers_removed == 0
        assert tracker.total_lines_discarded == 0
        assert tracker.original_character_count == 0
        assert tracker.final_character_count == 0
        assert len(tracker.discarded_items) == 0

    def test_add_discard_page_number(self):
        """Test adding page number discard."""
        tracker = DiscardTracker()
        tracker.add_discard(
            DiscardType.PAGE_NUMBER,
            "1",
            page=0,
            line=1,
            reason="Test page number"
        )
        assert tracker.page_numbers_removed == 1
        assert tracker.total_lines_discarded == 1
        assert len(tracker.discarded_items) == 1
        assert tracker.discarded_items[0].content == "1"

    def test_add_discard_header_footer(self):
        """Test adding header/footer discard."""
        tracker = DiscardTracker()
        tracker.add_discard(DiscardType.HEADER_FOOTER, "Header Text")
        assert tracker.headers_footers_removed == 1
        assert tracker.total_lines_discarded == 1

    def test_add_discard_arxiv_metadata(self):
        """Test adding arXiv metadata discard."""
        tracker = DiscardTracker()
        tracker.add_discard(DiscardType.ARXIV_METADATA, "arXiv:1234.5678")
        assert tracker.arxiv_metadata_removed == 1
        assert tracker.total_lines_discarded == 1

    def test_add_discard_multiple_types(self):
        """Test adding multiple different discard types."""
        tracker = DiscardTracker()
        tracker.add_discard(DiscardType.PAGE_NUMBER, "1")
        tracker.add_discard(DiscardType.HEADER_FOOTER, "Header")
        tracker.add_discard(DiscardType.ARXIV_METADATA, "arXiv:123")
        tracker.add_discard(DiscardType.SHORT_LINE, "x")

        assert tracker.page_numbers_removed == 1
        assert tracker.headers_footers_removed == 1
        assert tracker.arxiv_metadata_removed == 1
        assert tracker.short_lines_removed == 1
        assert tracker.total_lines_discarded == 4

    def test_get_summary(self):
        """Test get_summary method."""
        tracker = DiscardTracker()
        tracker.add_discard(DiscardType.PAGE_NUMBER, "1")
        tracker.add_discard(DiscardType.PAGE_NUMBER, "2")
        tracker.add_discard(DiscardType.SHORT_LINE, "x")

        summary = tracker.get_summary()
        assert summary["page_numbers"] == 2
        assert summary["short_lines"] == 1
        assert summary["total_discarded"] == 3
        assert summary["headers_footers"] == 0

    def test_get_statistics(self):
        """Test get_statistics method."""
        tracker = DiscardTracker()
        tracker.total_lines_processed = 100
        tracker.total_lines_discarded = 20
        tracker.original_character_count = 10000
        tracker.final_character_count = 8000

        stats = tracker.get_statistics()
        assert stats["total_lines_processed"] == 100
        assert stats["total_lines_discarded"] == 20
        assert stats["discard_rate_percent"] == 20.0
        assert stats["original_characters"] == 10000
        assert stats["final_characters"] == 8000
        assert stats["characters_discarded"] == 2000
        assert stats["character_reduction_percent"] == 20.0

    def test_get_statistics_no_lines_processed(self):
        """Test get_statistics with no lines processed."""
        tracker = DiscardTracker()
        stats = tracker.get_statistics()
        assert stats["discard_rate_percent"] == 0.0
        assert stats["character_reduction_percent"] == 0.0

    def test_get_statistics_rounding(self):
        """Test that statistics are properly rounded."""
        tracker = DiscardTracker()
        tracker.total_lines_processed = 3
        tracker.total_lines_discarded = 1
        tracker.original_character_count = 100
        tracker.final_character_count = 67

        stats = tracker.get_statistics()
        # 1/3 * 100 = 33.333... should round to 33.33
        assert stats["discard_rate_percent"] == 33.33
        # 33/100 * 100 = 33.0
        assert stats["character_reduction_percent"] == 33.0

    def test_multiple_discards_same_type(self):
        """Test adding multiple discards of the same type."""
        tracker = DiscardTracker()
        for i in range(5):
            tracker.add_discard(DiscardType.BIBLIOGRAPHY_ENTRY, f"Reference {i}")

        assert tracker.bibliography_entries_removed == 5
        assert tracker.total_lines_discarded == 5
        assert len(tracker.discarded_items) == 5

    def test_other_discard_type(self):
        """Test adding OTHER type discard."""
        tracker = DiscardTracker()
        tracker.add_discard(DiscardType.OTHER, "Unknown content")
        assert tracker.other_removed == 1
        assert tracker.total_lines_discarded == 1

    def test_export_log_creates_file(self, tmp_path):
        """Test that export_log creates a file."""
        tracker = DiscardTracker()
        tracker.total_lines_processed = 100
        tracker.original_character_count = 5000
        tracker.final_character_count = 4000
        tracker.add_discard(DiscardType.PAGE_NUMBER, "1")
        tracker.add_discard(DiscardType.SHORT_LINE, "x")

        output_file = tmp_path / "test_log.txt"
        tracker.export_log(str(output_file))

        assert output_file.exists()
        content = output_file.read_text()
        assert "DETAILED DISCARD LOG" in content
        assert "SUMMARY" in content
        assert "STATISTICS" in content

    def test_print_summary_does_not_raise(self, capsys):
        """Test that print_summary doesn't raise an error."""
        tracker = DiscardTracker()
        tracker.total_lines_processed = 100
        tracker.original_character_count = 5000
        tracker.final_character_count = 4000
        tracker.add_discard(DiscardType.PAGE_NUMBER, "1")

        # Should not raise
        tracker.print_summary()

        captured = capsys.readouterr()
        assert "DISCARD TRACKER SUMMARY" in captured.out
        assert "ITEMS DISCARDED BY TYPE" in captured.out


class TestDiscardTrackerIntegration:
    """Integration tests for DiscardTracker."""

    def test_full_workflow(self, tmp_path):
        """Test a complete workflow of tracking discards."""
        tracker = DiscardTracker()

        # Simulate processing
        tracker.total_lines_processed = 1000
        tracker.original_character_count = 50000

        # Add various discards
        for i in range(10):
            tracker.add_discard(DiscardType.PAGE_NUMBER, str(i))
        for i in range(5):
            tracker.add_discard(DiscardType.HEADER_FOOTER, f"Header {i}")
        for i in range(100):
            tracker.add_discard(DiscardType.BIBLIOGRAPHY_ENTRY, f"Ref {i}")

        tracker.final_character_count = 32000

        # Get summary
        summary = tracker.get_summary()
        assert summary["page_numbers"] == 10
        assert summary["headers_footers"] == 5
        assert summary["bibliography_entries"] == 100
        assert summary["total_discarded"] == 115

        # Get statistics
        stats = tracker.get_statistics()
        assert stats["total_lines_processed"] == 1000
        assert stats["total_lines_discarded"] == 115
        assert stats["characters_discarded"] == 18000

        # Export log
        output_file = tmp_path / "integration_log.txt"
        tracker.export_log(str(output_file))
        assert output_file.exists()
