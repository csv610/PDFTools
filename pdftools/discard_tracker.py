from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum


class DiscardType(Enum):
    """Types of content that can be discarded during extraction."""
    PAGE_NUMBER = "page_number"
    HEADER_FOOTER = "header_footer"
    ARXIV_METADATA = "arxiv_metadata"
    DATE_FOOTER = "date_footer"
    SEPARATOR_LINE = "separator_line"
    SHORT_LINE = "short_line"
    REFERENCES_SECTION = "references_section"
    BIBLIOGRAPHY_ENTRY = "bibliography_entry"
    OTHER = "other"


@dataclass
class DiscardedItem:
    """Represents a single discarded item."""
    discard_type: DiscardType
    content: str
    page_number: int = 0
    line_number: int = 0
    reason: str = ""

    def __str__(self) -> str:
        return f"[{self.discard_type.value}] Page {self.page_number}, Line {self.line_number}: {self.content[:50]}..."


@dataclass
class DiscardTracker:
    """Tracks all discarded content during PDF extraction."""

    # Counters by discard type
    page_numbers_removed: int = 0
    headers_footers_removed: int = 0
    arxiv_metadata_removed: int = 0
    date_footers_removed: int = 0
    separator_lines_removed: int = 0
    short_lines_removed: int = 0
    references_sections_removed: int = 0
    bibliography_entries_removed: int = 0
    other_removed: int = 0

    # Detailed tracking
    discarded_items: List[DiscardedItem] = field(default_factory=list)

    # Statistics
    total_lines_processed: int = 0
    total_lines_discarded: int = 0
    original_character_count: int = 0
    final_character_count: int = 0

    def add_discard(self, discard_type: DiscardType, content: str, page: int = 0,
                   line: int = 0, reason: str = "") -> None:
        """Add a discarded item to the tracker."""
        self.discarded_items.append(
            DiscardedItem(
                discard_type=discard_type,
                content=content,
                page_number=page,
                line_number=line,
                reason=reason
            )
        )

        # Update counters
        self.total_lines_discarded += 1
        if discard_type == DiscardType.PAGE_NUMBER:
            self.page_numbers_removed += 1
        elif discard_type == DiscardType.HEADER_FOOTER:
            self.headers_footers_removed += 1
        elif discard_type == DiscardType.ARXIV_METADATA:
            self.arxiv_metadata_removed += 1
        elif discard_type == DiscardType.DATE_FOOTER:
            self.date_footers_removed += 1
        elif discard_type == DiscardType.SEPARATOR_LINE:
            self.separator_lines_removed += 1
        elif discard_type == DiscardType.SHORT_LINE:
            self.short_lines_removed += 1
        elif discard_type == DiscardType.REFERENCES_SECTION:
            self.references_sections_removed += 1
        elif discard_type == DiscardType.BIBLIOGRAPHY_ENTRY:
            self.bibliography_entries_removed += 1
        else:
            self.other_removed += 1

    def get_summary(self) -> Dict[str, int]:
        """Get a summary of discarded items by type."""
        return {
            "page_numbers": self.page_numbers_removed,
            "headers_footers": self.headers_footers_removed,
            "arxiv_metadata": self.arxiv_metadata_removed,
            "date_footers": self.date_footers_removed,
            "separator_lines": self.separator_lines_removed,
            "short_lines": self.short_lines_removed,
            "references_sections": self.references_sections_removed,
            "bibliography_entries": self.bibliography_entries_removed,
            "other": self.other_removed,
            "total_discarded": self.total_lines_discarded,
        }

    def get_statistics(self) -> Dict[str, any]:
        """Get detailed statistics."""
        discard_rate = (self.total_lines_discarded / self.total_lines_processed * 100
                       if self.total_lines_processed > 0 else 0)
        char_reduction = (self.original_character_count - self.final_character_count)
        char_reduction_percent = (char_reduction / self.original_character_count * 100
                                 if self.original_character_count > 0 else 0)

        return {
            "total_lines_processed": self.total_lines_processed,
            "total_lines_discarded": self.total_lines_discarded,
            "discard_rate_percent": round(discard_rate, 2),
            "original_characters": self.original_character_count,
            "final_characters": self.final_character_count,
            "characters_discarded": char_reduction,
            "character_reduction_percent": round(char_reduction_percent, 2),
        }

    def print_summary(self) -> None:
        """Print a formatted summary of discards."""
        summary = self.get_summary()
        stats = self.get_statistics()

        print("=" * 80)
        print("DISCARD TRACKER SUMMARY")
        print("=" * 80)

        print("\n📊 ITEMS DISCARDED BY TYPE:")
        print("-" * 80)
        for key, count in summary.items():
            if key != "total_discarded" and count > 0:
                print(f"  {key.replace('_', ' ').title():<30} {count:5d} items")

        print(f"\n  {'TOTAL DISCARDED':<30} {summary['total_discarded']:5d} items")

        print("\n📈 STATISTICS:")
        print("-" * 80)
        print(f"  Lines processed:            {stats['total_lines_processed']:,}")
        print(f"  Lines discarded:            {stats['total_lines_discarded']:,} ({stats['discard_rate_percent']:.1f}%)")
        print(f"  Original characters:        {stats['original_characters']:,}")
        print(f"  Final characters:           {stats['final_characters']:,}")
        print(f"  Characters removed:         {stats['characters_discarded']:,} ({stats['character_reduction_percent']:.1f}%)")

        print("\n" + "=" * 80)

    def export_log(self, filename: str) -> None:
        """Export detailed discard log to file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("DETAILED DISCARD LOG\n")
            f.write("=" * 80 + "\n\n")

            # Summary
            summary = self.get_summary()
            stats = self.get_statistics()

            f.write("SUMMARY\n")
            f.write("-" * 80 + "\n")
            for key, count in summary.items():
                if key != "total_discarded" and count > 0:
                    f.write(f"{key.replace('_', ' ').title():<30} {count:5d}\n")
            f.write(f"\nTOTAL DISCARDED: {summary['total_discarded']}\n\n")

            # Statistics
            f.write("STATISTICS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Lines processed:    {stats['total_lines_processed']}\n")
            f.write(f"Lines discarded:    {stats['total_lines_discarded']} ({stats['discard_rate_percent']:.1f}%)\n")
            f.write(f"Original chars:     {stats['original_characters']:,}\n")
            f.write(f"Final chars:        {stats['final_characters']:,}\n")
            f.write(f"Chars removed:      {stats['characters_discarded']:,} ({stats['character_reduction_percent']:.1f}%)\n\n")

            # Detailed items
            f.write("DETAILED DISCARD LIST\n")
            f.write("=" * 80 + "\n\n")

            # Group by type
            by_type = {}
            for item in self.discarded_items:
                if item.discard_type not in by_type:
                    by_type[item.discard_type] = []
                by_type[item.discard_type].append(item)

            for discard_type in DiscardType:
                if discard_type in by_type:
                    f.write(f"\n{discard_type.value.upper()}\n")
                    f.write("-" * 80 + "\n")
                    for item in by_type[discard_type][:10]:  # Show first 10
                        f.write(f"  Page {item.page_number}, Line {item.line_number}: ")
                        f.write(f"{item.content[:70]}\n")
                        if item.reason:
                            f.write(f"    Reason: {item.reason}\n")
                    if len(by_type[discard_type]) > 10:
                        f.write(f"  ... and {len(by_type[discard_type]) - 10} more items\n")


# Example usage
if __name__ == "__main__":
    # Create tracker
    tracker = DiscardTracker()

    # Simulate some discards
    tracker.total_lines_processed = 1000
    tracker.original_character_count = 50000
    tracker.final_character_count = 32000

    tracker.add_discard(DiscardType.PAGE_NUMBER, "1", page=0, line=1)
    tracker.add_discard(DiscardType.PAGE_NUMBER, "2", page=1, line=50)
    tracker.add_discard(DiscardType.ARXIV_METADATA, "arXiv:1706.03762v7 [cs.CL]", page=0)
    tracker.add_discard(DiscardType.DATE_FOOTER, "2 Aug 2023", page=0)
    tracker.add_discard(DiscardType.SEPARATOR_LINE, "========", page=2)
    tracker.add_discard(DiscardType.SHORT_LINE, ".", page=3, reason="Too short")

    # Add many bibliography entries
    for i in range(134):
        tracker.add_discard(DiscardType.BIBLIOGRAPHY_ENTRY, f"[{i+1}] Author, Title, Journal", page=10+i//20)

    # Print summary
    tracker.print_summary()

    # Export log
    tracker.export_log("discard_log.txt")
    print("\nLog exported to discard_log.txt")
