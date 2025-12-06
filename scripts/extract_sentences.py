"""
Example: Extract sentences with detailed discard tracking.

This demonstrates how to integrate the DiscardTracker with extraction scripts
to document what content was removed during processing.
"""

import sys
from pathlib import Path

# Add pdftool directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "pdftool"))

import re
from discard_tracker import DiscardTracker, DiscardType
from pdftext_utils import (
    extract_and_clean, calculate_page_position, save_content_to_file,
    display_table, get_cli_parser
)


def extract_sentences(full_text, page_boundaries, tracker):
    """Extract sentences from cleaned text."""
    sentence_pattern = r'(?<=[.!?])\s+'
    raw_sentences = re.split(sentence_pattern, full_text)

    sentences = []
    page_starts = []
    page_ends = []
    char_pos = 0

    for sentence in raw_sentences:
        sentence = sentence.strip()

        # Skip very short strings
        if len(sentence) < 10:
            tracker.add_discard(DiscardType.SHORT_LINE, sentence, 0, 0,
                              "Sentence < 10 chars")
            continue

        # Skip sentence number artifacts
        if re.match(r'^\d+\s*$', sentence):
            tracker.add_discard(DiscardType.PAGE_NUMBER, sentence, 0, 0,
                              "Sentence is just a number")
            continue

        # Find position
        sentence_start = full_text.find(sentence, char_pos)
        if sentence_start == -1:
            sentence_start = char_pos

        sentence_end = sentence_start + len(sentence)

        # Determine pages
        start_page = calculate_page_position(sentence_start, page_boundaries)
        end_page = calculate_page_position(sentence_end, page_boundaries)

        sentences.append(sentence)
        page_starts.append(start_page)
        page_ends.append(end_page)

        char_pos = sentence_end

    tracker.final_character_count = sum(len(s) for s in sentences)
    return sentences, page_starts, page_ends




if __name__ == "__main__":
    parser = get_cli_parser(
        "Extract sentences with detailed discard tracking",
        "extracted_with_tracking.txt"
    )
    args = parser.parse_args()

    # Initialize tracker
    tracker = DiscardTracker()

    print("Extracting and cleaning PDF text...")
    full_text, page_boundaries = extract_and_clean(args.pdf_file, tracker)

    print("Extracting sentences...")
    sentences, page_starts, page_ends = extract_sentences(
        full_text, page_boundaries, tracker
    )

    print(f"Found {len(sentences)} sentences\n")

    if args.display:
        display_table(sentences, page_starts, page_ends, "Sentence")

    print(f"Saving sentences to {args.output}...")
    save_content_to_file(sentences, page_starts, page_ends, args.output, "Sentence")

    print(f"Saving tracking log to {args.track_log}...")
    tracker.export_log(args.track_log)

    print(f"\nDone! Extracted {len(sentences)} sentences")
    print(f"Saved to {args.output}")
    print(f"Tracking log saved to {args.track_log}")

    # Print summary
    tracker.print_summary()
