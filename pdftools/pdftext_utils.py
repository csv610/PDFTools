"""
Shared PDF extraction utilities for processing academic papers.

Provides common functions for cleaning PDF text and tracking discarded content.
"""

import argparse
import re
from pypdf import PdfReader
from discard_tracker import DiscardTracker, DiscardType


def extract_and_clean(pdf_path: str, tracker: DiscardTracker) -> tuple[str, list]:
    """Extract text from PDF and track what gets discarded.

    Args:
        pdf_path: Path to the PDF file
        tracker: DiscardTracker instance to log removals

    Returns:
        Tuple of (cleaned_text, page_boundaries)
    """
    reader = PdfReader(pdf_path)
    page_boundaries = [0]
    full_text = ""

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            cleaned = clean_page_text(text, page_num, tracker)
            full_text += cleaned + "\n"
        page_boundaries.append(len(full_text))

    tracker.original_character_count = len(full_text)

    # Remove references and track
    full_text = remove_references(full_text, tracker)

    return full_text, page_boundaries


def clean_page_text(text: str, page_num: int, tracker: DiscardTracker) -> str:
    """Remove artifacts and track what was removed.

    Args:
        text: Raw text from a PDF page
        page_num: Page number for tracking
        tracker: DiscardTracker instance

    Returns:
        Cleaned text with artifacts removed
    """
    lines = text.split('\n')
    cleaned_lines = []
    line_num = 0

    for line in lines:
        line_num += 1
        stripped = line.strip()

        # Skip empty lines (don't track)
        if not stripped:
            continue

        tracker.total_lines_processed += 1

        # Check page numbers
        if re.match(r'^\d{1,3}$', stripped):
            tracker.add_discard(DiscardType.PAGE_NUMBER, stripped, page_num, line_num,
                              "Standalone page number")
            continue

        # Check arXiv metadata
        if re.match(r'^arXiv:\d+\.\d+', stripped):
            tracker.add_discard(DiscardType.ARXIV_METADATA, stripped, page_num, line_num,
                              "arXiv header/footer")
            continue

        # Check date footers
        if re.match(r'^\d+\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}$',
                   stripped, re.IGNORECASE):
            tracker.add_discard(DiscardType.DATE_FOOTER, stripped, page_num, line_num,
                              "Date footer line")
            continue

        # Check separator lines
        if re.match(r'^[=\-*\s]{3,}$', stripped):
            tracker.add_discard(DiscardType.SEPARATOR_LINE, stripped, page_num, line_num,
                              "Separator/divider line")
            continue

        # Check short lines
        if len(stripped) < 3:
            tracker.add_discard(DiscardType.SHORT_LINE, stripped, page_num, line_num,
                              "Too short (< 3 chars)")
            continue

        # Keep the line
        cleaned_lines.append(line)

    # Normalize whitespace
    text_joined = '\n'.join(cleaned_lines)
    text_joined = re.sub(r' {2,}', ' ', text_joined)

    return text_joined


def remove_references(text: str, tracker: DiscardTracker) -> str:
    """Remove references section and track what was removed.

    Args:
        text: Full document text
        tracker: DiscardTracker instance

    Returns:
        Text with references section removed
    """
    ref_patterns = [
        r'^\s*(?:References|Bibliography|REFERENCES|BIBLIOGRAPHY)\s*$',
    ]

    lines = text.split('\n')
    ref_start_idx = None

    for i, line in enumerate(lines):
        for pattern in ref_patterns:
            if re.match(pattern, line.strip(), re.IGNORECASE):
                ref_start_idx = i
                break
        if ref_start_idx is not None:
            break

    if ref_start_idx is not None:
        # Track the references section header
        tracker.add_discard(DiscardType.REFERENCES_SECTION,
                          lines[ref_start_idx], ref_start_idx, 0,
                          "References section header")

        # Track bibliography entries
        removed_lines = lines[ref_start_idx:]
        for i, line in enumerate(removed_lines[1:], ref_start_idx + 1):
            stripped = line.strip()
            if stripped and not stripped.startswith('='):
                tracker.add_discard(DiscardType.BIBLIOGRAPHY_ENTRY, stripped, 0, i,
                                  "Bibliography/reference entry")

        # Remove everything from References onwards
        text = '\n'.join(lines[:ref_start_idx])

    return text


def calculate_page_position(position: int, page_boundaries: list) -> int:
    """Calculate page number for a given character position.

    Args:
        position: Character position in text
        page_boundaries: List of page boundary positions

    Returns:
        Page number (0-indexed)
    """
    return sum(1 for b in page_boundaries[1:] if b <= position)


def save_content_to_file(items: list, starts: list, ends: list, output_file: str,
                        item_name: str) -> None:
    """Save extracted items (sentences/paragraphs) to file.

    Args:
        items: List of text items to save
        starts: List of start page numbers
        ends: List of end page numbers
        output_file: Path to output file
        item_name: Name for item type (e.g., "Sentence", "Paragraph")
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, (item, start_page, end_page) in enumerate(
            zip(items, starts, ends), 1
        ):
            if start_page == end_page:
                f.write(f"[{item_name} {i} - Page {start_page}]\n")
            else:
                f.write(f"[{item_name} {i} - Pages {start_page}-{end_page}]\n")
            f.write(item)
            f.write("\n" + "=" * 80 + "\n\n")


def display_table(items: list, starts: list, ends: list, item_name: str) -> None:
    """Display items in table format.

    Args:
        items: List of text items
        starts: List of start page numbers
        ends: List of end page numbers
        item_name: Name for item type (e.g., "Sentence", "Paragraph")
    """
    print("=" * 130)
    print(f"{item_name:<85} {'Pages':<15} {'Length':<10}")
    print("=" * 130)
    for item, start_page, end_page in zip(items, starts, ends):
        item_display = item.replace('\n', ' ')[:85]
        item_length = len(item)
        if start_page == end_page:
            pages_str = str(start_page)
        else:
            pages_str = f"{start_page}-{end_page}"
        print(f"{item_display:<85} {pages_str:<15} {item_length:<10}")
    print("=" * 130 + "\n")


def get_cli_parser(description: str, default_output: str) -> argparse.ArgumentParser:
    """Create argument parser for extraction scripts.

    Args:
        description: Script description
        default_output: Default output filename

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("pdf_file", help="Path to the PDF file")
    parser.add_argument("-o", "--output", default=default_output,
                       help="Output file path")
    parser.add_argument("-t", "--track-log", default="discard_tracking.txt",
                       help="Discard tracking log file")
    parser.add_argument("-d", "--display", action="store_true",
                       help="Display items in table format")
    return parser
