"""Merge multiple PDF files into one."""

from PyPDF2 import PdfMerger


def merge_pdfs(input_files, output_file):
    """Merge multiple PDF files into a single output file.

    Args:
        input_files: List of PDF file paths to merge
        output_file: Path to the output merged PDF file
    """
    merger = PdfMerger()

    try:
        for file in input_files:
            merger.append(file)

        merger.write(output_file)
    finally:
        merger.close()


def main():
    """Example usage of merge_pdfs function."""
    input_files = ["file1.pdf", "file2.pdf", "file3.pdf"]
    output_file = "merged.pdf"
    merge_pdfs(input_files, output_file)


if __name__ == "__main__":
    main()
