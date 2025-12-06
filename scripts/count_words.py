from pypdf import PdfReader
from pathlib import Path
import argparse
import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)


def count_words_in_pdf(
    pdf_path: str,
    start_page: int = 1,
    end_page: Optional[int] = None,
) -> Optional[dict]:
    """
    Count the number of words in a PDF file.

    Uses a more sophisticated word counting algorithm that:
    - Splits on whitespace and common punctuation
    - Filters out empty strings
    - Handles multi-line text properly

    Args:
        pdf_path: Path to the PDF file
        start_page: Starting page number (1-indexed, default: 1)
        end_page: Ending page number inclusive (1-indexed, default: last page)

    Returns:
        Dictionary with word count and page information, or None if error occurs

    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        ValueError: If the PDF is invalid or page range is invalid
    """
    input_path = Path(pdf_path)

    if not input_path.is_file():
        raise FileNotFoundError(f"The PDF file '{pdf_path}' does not exist.")

    if input_path.suffix.lower() != ".pdf":
        raise ValueError(f"The file '{pdf_path}' is not a PDF file.")

    if start_page < 1:
        raise ValueError(f"start_page must be at least 1, got {start_page}")

    try:
        with open(input_path, "rb") as file:
            reader = PdfReader(file)
            total_pages = len(reader.pages)

            if total_pages == 0:
                raise ValueError("The PDF file is empty.")

            # Validate and set end_page
            actual_end_page = end_page if end_page is not None else total_pages

            if start_page > total_pages:
                raise ValueError(
                    f"start_page ({start_page}) exceeds total pages ({total_pages})"
                )

            if actual_end_page < start_page:
                raise ValueError(
                    f"end_page ({actual_end_page}) must be >= start_page ({start_page})"
                )

            if actual_end_page > total_pages:
                raise ValueError(
                    f"end_page ({actual_end_page}) exceeds total pages ({total_pages})"
                )

            word_count = 0
            page_count = 0

            # Convert to 0-indexed
            start_idx = start_page - 1
            end_idx = actual_end_page

            logger.info(
                f"Counting words in pages {start_page}-{actual_end_page} of {total_pages}"
            )

            for page_idx in range(start_idx, end_idx):
                try:
                    page = reader.pages[page_idx]
                    text = page.extract_text()

                    if text:
                        # More sophisticated word counting
                        # Split on whitespace and punctuation, filter empty strings
                        words = [
                            word
                            for word in re.split(r"[\s\-–—]+", text)
                            if word.strip()
                        ]
                        word_count += len(words)
                        page_count += 1
                        logger.debug(
                            f"Page {page_idx + 1}: {len(words)} words"
                        )

                except Exception as e:
                    logger.warning(
                        f"Could not extract text from page {page_idx + 1}: {e}"
                    )

            return {
                "total_words": word_count,
                "pages_processed": page_count,
                "start_page": start_page,
                "end_page": actual_end_page,
                "total_pages": total_pages,
            }

    except FileNotFoundError:
        raise
    except Exception as e:
        raise RuntimeError(f"Failed to count words in PDF: {e}") from e


def main() -> None:
    """Main entry point for the word counting tool."""
    parser = argparse.ArgumentParser(
        description="Count words in a PDF file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python count_words.py -i document.pdf\n"
               "  python count_words.py -i document.pdf -s 5 -e 20\n"
               "  python count_words.py -i document.pdf -v",
    )
    parser.add_argument(
        "--input_file",
        "-i",
        type=str,
        required=True,
        help="Path to the PDF file (required)",
    )
    parser.add_argument(
        "--start_page",
        "-s",
        type=int,
        default=1,
        help="Starting page number (1-indexed, default: 1)",
    )
    parser.add_argument(
        "--end_page",
        "-e",
        type=int,
        default=None,
        help="Ending page number inclusive (1-indexed, default: last page)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging output",
    )

    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    try:
        logger.info("Starting word count process")
        logger.info(f"Input file: {args.input_file}")
        if args.start_page != 1 or args.end_page is not None:
            logger.info(
                f"Page range: {args.start_page}-{args.end_page if args.end_page else 'end'}"
            )

        result = count_words_in_pdf(
            args.input_file,
            start_page=args.start_page,
            end_page=args.end_page,
        )

        if result:
            print(f"\nWord Count Results:")
            print(f"  Total words: {result['total_words']:,}")
            print(
                f"  Pages: {result['start_page']}-{result['end_page']} "
                f"({result['pages_processed']}/{result['end_page'] - result['start_page'] + 1} pages processed)"
            )
            logger.info(f"Word count completed successfully")
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        exit(1)
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    main()

