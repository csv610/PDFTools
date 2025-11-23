# PDFTools

A comprehensive Python toolkit for PDF manipulation and analysis. Easily convert, split, merge, and analyze PDF files with simple command-line tools.

## Features

- **PDF to Text Extraction** - Extract text content from PDF files
- **Word Counting** - Count words in PDF documents with page range support
- **PDF Splitting** - Split large PDFs into smaller chunks
- **Page Removal** - Remove specific pages from PDF documents
- **PDF to Image Conversion** - Convert PDF pages to high-resolution images
- **PDF Merging** - Merge multiple PDF files into one

## Installation

### Requirements
- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/PDFTools.git
cd PDFTools
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### PDF to Text Extraction

Extract all text from a PDF file:
```bash
python pdf2text.py document.pdf
```

### Word Counting

Count words in an entire PDF:
```bash
python count_words.py -i document.pdf
```

Count words in specific pages:
```bash
python count_words.py -i document.pdf -s 1 -e 10
```

Enable verbose output:
```bash
python count_words.py -i document.pdf -v
```

**Output:**
```
Word Count Results:
  Total words: 108,596
  Pages: 1-442 (430/442 pages processed)
```

### Splitting PDFs

Split a PDF into 10-page chunks (default):
```bash
python split_pdf_file.py -i large_document.pdf
```

Split with custom page count:
```bash
python split_pdf_file.py -i large_document.pdf -p 20
```

Split specific page range into 5-page chunks:
```bash
python split_pdf_file.py -i large_document.pdf -p 5 -s 10 -e 50
```

**Output files:** `splits/split_001.pdf`, `splits/split_002.pdf`, etc.

### Removing Pages

Remove specific pages:
```bash
python remove_pdf_pages.py -i input.pdf -o output.pdf -p 1,3,5
```

Remove page ranges:
```bash
python remove_pdf_pages.py -i input.pdf -o output.pdf -p 1-5,10-15
```

Mixed format (pages and ranges):
```bash
python remove_pdf_pages.py -i input.pdf -o output.pdf -p 1,3-5,7,20-25
```

### Converting to Images

Convert all pages to images:
```bash
python pdfpages2images.py input.pdf
```

**Output directory:** `images/page_001.png`, `images/page_002.png`, etc.

Customize DPI (default 300):
```bash
python pdfpages2images.py input.pdf --dpi 150
```

### Merging PDFs

Merge multiple PDFs into one:
```bash
python merge_pdfs.py file1.pdf file2.pdf file3.pdf merged.pdf
```

## Tools Reference

| Tool | Purpose | Usage |
|------|---------|-------|
| `pdf2text.py` | Extract text from PDF | `python pdf2text.py document.pdf` |
| `count_words.py` | Count words with options | `python count_words.py -i document.pdf [-s 1 -e 10]` |
| `split_pdf_file.py` | Split PDF into chunks | `python split_pdf_file.py -i file.pdf [-p 10]` |
| `remove_pdf_pages.py` | Remove specific pages | `python remove_pdf_pages.py -i input.pdf -o output.pdf -p 1,3-5` |
| `pdfpages2images.py` | Convert pages to images | `python pdfpages2images.py input.pdf` |
| `merge_pdfs.py` | Merge multiple PDFs | `python merge_pdfs.py file1.pdf file2.pdf output.pdf` |

## Command-Line Options

### count_words.py
- `-i, --input_file` (required): Path to the PDF file
- `-s, --start_page` (default: 1): Starting page number (1-indexed)
- `-e, --end_page` (default: last page): Ending page number (1-indexed)
- `-v, --verbose`: Enable verbose logging

### split_pdf_file.py
- `-i, --input_file` (required): Path to the input PDF
- `-p, --pages_per_split` (default: 10): Pages per output file
- `-d, --output_directory` (default: splits): Output directory
- `-s, --start_page` (default: 1): Starting page
- `-e, --end_page` (default: last): Ending page
- `-v, --verbose`: Enable verbose logging

### remove_pdf_pages.py
- `-i, --input_file` (required): Path to the input PDF
- `-o, --output_file` (required): Path to save output
- `-p, --pages` (required): Pages to remove (e.g., "1,3-5,7")
- `-v, --verbose`: Enable verbose logging

### pdfpages2images.py
- Input file (positional argument)
- `--dpi` (default: 300): Resolution in DPI
- `--chunk_size` (default: 5): Pages to process at once

## Examples

### Extract text from first 10 pages and save to file
```bash
python pdf2text.py document.pdf | head -c 5000 > output.txt
```

### Count words in chapters 2-5
```bash
python count_words.py -i book.pdf -s 10 -e 50
```

### Create 50-page splits from large document
```bash
python split_pdf_file.py -i huge_document.pdf -p 50 -d output/splits
```

### Remove cover and back pages
```bash
python remove_pdf_pages.py -i book.pdf -o book_clean.pdf -p 1,420-425
```

### Convert first 50 pages to high-resolution images
```bash
python pdfpages2images.py document.pdf
python split_pdf_file.py -i document.pdf -p 50 | head -1
```

## Error Handling

All tools include comprehensive error handling:
- File validation (checks if PDF exists and is valid)
- Page range validation
- Proper error messages to stderr
- Exit codes for integration with scripts

Example error output:
```
Error: File not found: /path/to/nonexistent.pdf
```

## Dependencies

- `PyPDF2` / `pypdf` - PDF reading and manipulation
- `pdf2image` - PDF to image conversion
- `Pillow` - Image processing

See `requirements.txt` for complete list and versions.

## Troubleshooting

### ModuleNotFoundError
Install missing dependencies:
```bash
pip install -r requirements.txt
```

### PDF processing fails
- Ensure PDF is not corrupted: try opening it in a PDF viewer
- Some PDFs with scanned images may have limited text extraction
- Try with verbose mode to see detailed error messages

### Image conversion is slow
- Large PDFs take time to convert to images
- Reduce DPI value (e.g., `--dpi 150`) for faster processing
- The default DPI is 300 for high quality

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Created with Python and PDF processing excellence.

## Acknowledgments

- [PyPDF](https://github.com/py-pdf/pypdf) - PDF manipulation library
- [pdf2image](https://github.com/Belval/pdf2image) - PDF to image conversion
