from pypdf import PdfReader, PdfWriter
from pathlib import Path
import argparse
import logging
from typing import List

logger = logging.getLogger(__name__)


def split_pdf(
    input_file: str,
    pages_per_split: int,
    start_page: int = 1,
    end_page: int | None = None,
) -> List[PdfWriter]:
    """
    Split a PDF file into multiple smaller PDFs.

    Args:
        input_file: Path to the input PDF file
        pages_per_split: Number of pages per output PDF
        start_page: Starting page number (1-indexed, default: 1)
        end_page: Ending page number inclusive (1-indexed, default: last page)

    Returns:
        List of PdfWriter objects containing the split PDFs

    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the PDF is empty, pages_per_split is invalid, or page range is invalid
    """
    if pages_per_split <= 0:
        raise ValueError("pages_per_split must be greater than 0")

    input_path = Path(input_file)

    if not input_path.is_file():
        raise FileNotFoundError(f"The input file '{input_file}' does not exist.")

    if input_path.suffix.lower() != ".pdf":
        raise ValueError(f"The file '{input_file}' is not a PDF file.")

    try:
        with open(input_path, "rb") as infile:
            input_pdf = PdfReader(infile)
            total_pages = len(input_pdf.pages)

            if total_pages == 0:
                raise ValueError("The input PDF file is empty.")

            # Validate page range
            if start_page < 1:
                raise ValueError(f"start_page must be at least 1, got {start_page}")

            if start_page > total_pages:
                raise ValueError(
                    f"start_page ({start_page}) exceeds total pages ({total_pages})"
                )

            # Set end_page to total_pages if not specified
            actual_end_page = end_page if end_page is not None else total_pages

            if actual_end_page < start_page:
                raise ValueError(
                    f"end_page ({actual_end_page}) must be >= start_page ({start_page})"
                )

            if actual_end_page > total_pages:
                raise ValueError(
                    f"end_page ({actual_end_page}) exceeds total pages ({total_pages})"
                )

            # Convert to 0-indexed for internal processing
            start_idx = start_page - 1
            end_idx = actual_end_page

            pages_to_split = end_idx - start_idx
            logger.info(
                f"Splitting PDF pages {start_page}-{actual_end_page} "
                f"({pages_to_split} pages) into chunks of {pages_per_split}"
            )
            split_pdfs = []

            for start in range(start_idx, end_idx, pages_per_split):
                end = min(start + pages_per_split, end_idx)
                output_pdf = PdfWriter()

                for page_idx in range(start, end):
                    try:
                        output_pdf.add_page(input_pdf.pages[page_idx])
                    except Exception as e:
                        logger.warning(f"Could not add page {page_idx + 1}: {e}")

                split_pdfs.append(output_pdf)
                logger.debug(f"Created split with pages {start + 1}-{end}")

        return split_pdfs
    except FileNotFoundError:
        raise
    except Exception as e:
        raise RuntimeError(f"Failed to split PDF: {e}") from e

def save_split_pdfs(split_pdfs: List[PdfWriter], output_directory: str) -> int:
    """
    Save split PDFs to the output directory.

    Args:
        split_pdfs: List of PdfWriter objects to save
        output_directory: Directory to store the output PDFs

    Returns:
        Number of PDFs saved

    Raises:
        OSError: If the output directory cannot be created or files cannot be written
        ValueError: If split_pdfs is empty
    """
    if not split_pdfs:
        raise ValueError("No PDFs to save")

    output_dir = Path(output_directory)

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise OSError(f"Failed to create output directory '{output_directory}': {e}") from e

    saved_count = 0
    for index, output_pdf in enumerate(split_pdfs, start=1):
        output_file = output_dir / f"split_{index:03d}.pdf"

        try:
            with open(output_file, "wb") as outfile:
                output_pdf.write(outfile)
            logger.info(f"Created: {output_file}")
            saved_count += 1
        except Exception as e:
            logger.error(f"Failed to write {output_file}: {e}")
            raise OSError(f"Failed to write PDF file '{output_file}': {e}") from e

    logger.info(f"Successfully saved {saved_count} PDF files")
    return saved_count

def main_split_pdf() -> None:
    """Main entry point for the PDF splitting tool."""
    parser = argparse.ArgumentParser(
        description="Split a PDF file into multiple smaller PDFs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python split_pdf_file.py -i document.pdf\n"
               "  python split_pdf_file.py -i document.pdf -p 5 -d output/",
    )
    parser.add_argument(
        "--input_file",
        "-i",
        type=str,
        required=True,
        help="Path to the input PDF file (required)",
    )
    parser.add_argument(
        "--output_directory",
        "-d",
        type=str,
        default="splits",
        help="Directory to store the split PDF files (default: 'splits')",
    )
    parser.add_argument(
        "--pages_per_split",
        "-p",
        type=int,
        default=10,
        help="Number of pages per split (default: 10)",
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
        logger.info("Starting PDF split process")
        logger.info(f"Input file: {args.input_file}")
        logger.info(f"Output directory: {args.output_directory}")
        logger.info(f"Pages per split: {args.pages_per_split}")
        if args.start_page != 1 or args.end_page is not None:
            logger.info(
                f"Page range: {args.start_page}-{args.end_page if args.end_page else 'end'}"
            )

        split_pdfs = split_pdf(
            args.input_file,
            args.pages_per_split,
            start_page=args.start_page,
            end_page=args.end_page,
        )
        saved_count = save_split_pdfs(split_pdfs, args.output_directory)

        logger.info(f"PDF splitting completed successfully! {saved_count} files created.")
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
    main_split_pdf()
