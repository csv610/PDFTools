"""
Extract paragraphs from PDF with detailed discard tracking.

Tracks and documents what content is removed during extraction process.
"""

import sys
from pathlib import Path

# Add pdftool directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "pdftool"))

import re
from discard_tracker import DiscardTracker
from pdftext_utils import (
    extract_and_clean, calculate_page_position, save_content_to_file,
    display_table, get_cli_parser
)


def extract_all_paragraphs(full_text, page_boundaries, tracker):
    """Extract paragraphs by section headers."""
    lines = full_text.split('\n')
    paragraphs = []
    page_starts = []
    page_ends = []
    current = []
    char_start = 0

    def save_paragraph(para_lines, min_length=20):
        """Helper to save a paragraph if it's long enough."""
        nonlocal char_start
        para_text = '\n'.join(para_lines).strip()
        if len(para_text) >= min_length:
            para_start = full_text.find(para_text, char_start)
            para_end = para_start + len(para_text) if para_start != -1 else char_start

            start_page = calculate_page_position(para_start, page_boundaries)
            end_page = calculate_page_position(para_end, page_boundaries)

            paragraphs.append(para_text)
            page_starts.append(start_page)
            page_ends.append(end_page)
            char_start = para_end

    for i, line in enumerate(lines):
        # Check if line looks like a section header (starts with digit(s) and a period)
        is_section_header = (
            line.strip() and
            line.strip()[0].isdigit() and
            '.' in line[:5] and
            len(current) > 0  # Only treat as header if we have accumulated content
        )

        if is_section_header:
            save_paragraph(current)
            current = [line]
        else:
            current.append(line)

    # Don't forget the last group
    if current:
        save_paragraph(current)

    tracker.final_character_count = sum(len(p) for p in paragraphs)
    return paragraphs, page_starts, page_ends




if __name__ == "__main__":
    parser = get_cli_parser(
        "Extract paragraphs with detailed discard tracking",
        "extracted_paragraphs.txt"
    )
    args = parser.parse_args()

    # Initialize tracker
    tracker = DiscardTracker()

    print("Extracting and cleaning PDF text...")
    full_text, page_boundaries = extract_and_clean(args.pdf_file, tracker)

    print("Extracting paragraphs...")
    paragraphs, page_starts, page_ends = extract_all_paragraphs(
        full_text, page_boundaries, tracker
    )

    print(f"Found {len(paragraphs)} paragraphs\n")

    if args.display:
        display_table(paragraphs, page_starts, page_ends, "Paragraph")

    print(f"Saving paragraphs to {args.output}...")
    save_content_to_file(paragraphs, page_starts, page_ends, args.output, "Paragraph")

    print(f"Saving tracking log to {args.track_log}...")
    tracker.export_log(args.track_log)

    print(f"\nDone! Extracted {len(paragraphs)} paragraphs")
    print(f"Saved to {args.output}")
    print(f"Tracking log saved to {args.track_log}")

    # Print summary
    tracker.print_summary()
