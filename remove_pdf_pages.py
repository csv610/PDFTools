from pypdf import PdfReader, PdfWriter
from pathlib import Path
import argparse
import logging
from typing import List, Set

logger = logging.getLogger(__name__)


def parse_page_numbers(page_input: str, total_pages: int) -> Set[int]:
    """
    Parse page numbers from user input.

    Supports formats:
    - Single pages: "1,3,5"
    - Ranges: "1-5,10-15"
    - Mixed: "1,3-5,7"

    Args:
        page_input: Comma-separated page numbers or ranges (1-indexed)
        total_pages: Total number of pages in the PDF

    Returns:
        Set of 0-indexed page numbers to remove

    Raises:
        ValueError: If page numbers are invalid or out of range
    """
    pages = set()

    for part in page_input.split(","):
        part = part.strip()
        if not part:
            continue

        if "-" in part:
            # Handle range like "1-5"
            try:
                start, end = part.split("-", 1)
                start = int(start.strip())
                end = int(end.strip())

                if start < 1 or end < 1:
                    raise ValueError(
                        f"Page numbers must be >= 1, got range {start}-{end}"
                    )

                if start > total_pages or end > total_pages:
                    raise ValueError(
                        f"Page range {start}-{end} exceeds total pages ({total_pages})"
                    )

                if start > end:
                    raise ValueError(
                        f"Invalid range {start}-{end}: start must be <= end"
                    )

                # Convert to 0-indexed and add to set
                pages.update(range(start - 1, end))

            except ValueError as e:
                raise ValueError(f"Invalid page range '{part}': {e}") from e
        else:
            # Handle single page number
            try:
                page_num = int(part)

                if page_num < 1:
                    raise ValueError(f"Page numbers must be >= 1, got {page_num}")

                if page_num > total_pages:
                    raise ValueError(
                        f"Page {page_num} exceeds total pages ({total_pages})"
                    )

                # Convert to 0-indexed
                pages.add(page_num - 1)

            except ValueError as e:
                raise ValueError(f"Invalid page number '{part}': {e}") from e

    if not pages:
        raise ValueError("No valid pages specified to remove")

    return pages


def remove_pages(
    input_file: str,
    output_file: str,
    pages_to_remove: str,
) -> int:
    """
    Remove specified pages from a PDF file.

    Args:
        input_file: Path to the input PDF file
        output_file: Path to save the output PDF file
        pages_to_remove: Comma-separated page numbers or ranges to remove (1-indexed)

    Returns:
        Number of pages in the output PDF

    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the PDF is invalid or page numbers are invalid
        OSError: If output file cannot be written
    """
    input_path = Path(input_file)

    if not input_path.is_file():
        raise FileNotFoundError(f"The input file '{input_file}' does not exist.")

    if input_path.suffix.lower() != ".pdf":
        raise ValueError(f"The file '{input_file}' is not a PDF file.")

    try:
        with open(input_path, "rb") as file:
            reader = PdfReader(file)
            total_pages = len(reader.pages)

            if total_pages == 0:
                raise ValueError("The input PDF file is empty.")

            logger.info(f"Loading PDF with {total_pages} pages")

            # Parse page numbers
            pages_idx = parse_page_numbers(pages_to_remove, total_pages)

            logger.info(
                f"Removing {len(pages_idx)} page(s): "
                f"{sorted([p + 1 for p in pages_idx])}"
            )

            # Create output PDF with remaining pages
            writer = PdfWriter()
            pages_kept = 0

            for page_num in range(total_pages):
                if page_num not in pages_idx:
                    try:
                        page = reader.pages[page_num]
                        writer.add_page(page)
                        pages_kept += 1
                        logger.debug(f"Kept page {page_num + 1}")
                    except Exception as e:
                        logger.warning(f"Could not process page {page_num + 1}: {e}")
                else:
                    logger.debug(f"Removed page {page_num + 1}")

            # Write output PDF
            output_path = Path(output_file)
            try:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as outfile:
                    writer.write(outfile)
                logger.info(f"Saved PDF with {pages_kept} pages to {output_path}")
                return pages_kept
            except Exception as e:
                raise OSError(f"Failed to write output file '{output_file}': {e}") from e

    except FileNotFoundError:
        raise
    except Exception as e:
        raise RuntimeError(f"Failed to remove pages from PDF: {e}") from e


def main() -> None:
    """Main entry point for the page removal tool."""
    parser = argparse.ArgumentParser(
        description="Remove specified pages from a PDF file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Page Number Formats:\n"
               "  Single pages:  -p 1,3,5\n"
               "  Ranges:        -p 1-5,10-15\n"
               "  Mixed:         -p 1,3-5,7\n"
               "\nExamples:\n"
               "  python remove_pdf_pages.py -i input.pdf -o output.pdf -p 1,3\n"
               "  python remove_pdf_pages.py -i input.pdf -o output.pdf -p 5-10\n"
               "  python remove_pdf_pages.py -i input.pdf -o output.pdf -p 1-3,10-15,20",
    )
    parser.add_argument(
        "--input_file",
        "-i",
        type=str,
        required=True,
        help="Path to the input PDF file (required)",
    )
    parser.add_argument(
        "--output_file",
        "-o",
        type=str,
        required=True,
        help="Path to save the output PDF file (required)",
    )
    parser.add_argument(
        "--pages",
        "-p",
        type=str,
        required=True,
        help="Page numbers to remove (1-indexed, comma-separated, supports ranges)",
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
        logger.info("Starting page removal process")
        logger.info(f"Input file: {args.input_file}")
        logger.info(f"Output file: {args.output_file}")
        logger.info(f"Pages to remove: {args.pages}")

        pages_remaining = remove_pages(
            args.input_file,
            args.output_file,
            args.pages,
        )

        print(f"\nPage Removal Results:")
        print(f"  Pages removed: {args.pages}")
        print(f"  Remaining pages: {pages_remaining}")
        logger.info("Page removal completed successfully")

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        exit(1)
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        exit(1)
    except OSError as e:
        logger.error(f"File I/O error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    main()

