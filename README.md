# PDFTools

A comprehensive Python package for PDF processing, text extraction, content analysis, and visualization. Extract and clean PDF content while tracking what gets removed during processing.

## Features

- **PDF Text Extraction** - Extract clean, processed text from PDFs with automatic artifact removal
- **Content Tracking** - Track exactly what content is removed and why during processing
- **Text Cleaning** - Automatic removal of page numbers, headers, footers, and other artifacts
- **Reference Management** - Identify and remove bibliography/references sections
- **Sentence/Paragraph Extraction** - Extract structured content (sentences, paragraphs, chapters)
- **Word Counting** - Count words in PDF files with page range support
- **PDF Manipulation** - Split, merge, remove pages from PDFs
- **Image Conversion** - Convert PDF pages to images
- **PDF Highlighting** - Programmatically highlight text in PDF documents
- **Web-Based Viewer** - Interactive PDF viewer built with Streamlit
- **Comprehensive Testing** - 194 passing tests with real PDF file testing

## Installation

### Requirements
- Python 3.8+
- pypdf (PDF processing)
- pdf2image (image conversion)
- Pillow (image handling)
- python-dotenv (environment configuration)
- PyMuPDF (fitz) (PDF highlighting and advanced viewing)
- Streamlit (web-based viewer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/csv610/PDFTools.git
cd PDFTools
```

2. Create a virtual environment:
```bash
python -m venv pdfenv
source pdfenv/bin/activate  # On Windows: pdfenv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```

## Quick Start

### Run the Web-Based PDF Viewer

```bash
# Run the app
streamlit run pdftools/sl_pdfviewer.py
```

The viewer will open at `http://localhost:8501` with features like:
- Single and double-page viewing
- Zoom control (50% - 1000%)
- Page rotation
- Text search with highlighting
- Night mode for comfortable reading

### Highlight Text in PDF

```python
from pdftools.pdf_highlighter import Highlighter

highlighter = Highlighter()
highlighter.highlight_words("input.pdf", ["important", "keywords"], "output.pdf")
```

### Extract and Clean PDF Text

```python
from pdftools.pdftext_utils import extract_and_clean
from pdftools.discard_tracker import DiscardTracker

# Initialize tracker to log what gets removed
tracker = DiscardTracker()

# Extract and clean text from PDF
text, page_boundaries = extract_and_clean("document.pdf", tracker)

# Get statistics on what was removed
stats = tracker.get_statistics()
print(f"Original characters: {stats['original_characters']}")
print(f"Final characters: {stats['final_characters']}")
print(f"Removed: {stats['character_reduction_percent']}%")

# Save tracking log
tracker.export_log("tracking_report.txt")
```

### Count Words in PDF

```python
from pdftools.count_words import count_words_in_pdf

# Count all words
result = count_words_in_pdf("document.pdf")
print(f"Total words: {result['total_words']}")

# Count specific page range
result = count_words_in_pdf("document.pdf", start_page=5, end_page=20)
print(f"Words on pages 5-20: {result['total_words']}")
```

### Extract Sentences or Paragraphs

```python
from pdftools.extract_sentences import extract_sentences
from pdftools.pdftext_utils import extract_and_clean
from pdftools.discard_tracker import DiscardTracker

tracker = DiscardTracker()
text, boundaries = extract_and_clean("document.pdf", tracker)

# Extract sentences
sentences, starts, ends = extract_sentences(text, boundaries, tracker)

# sentences: list of extracted sentences
# starts: page where each sentence starts
# ends: page where each sentence ends
```

### PDF Manipulation

```python
from pdftools.split_pdf_file import split_pdf
from pdftools.merge_pdfs import merge_pdfs
from pdftools.remove_pdf_pages import remove_pdf_pages

# Split PDF into smaller files
split_pdf("large.pdf", pages_per_split=10, output_dir="split_files")

# Merge PDFs
merge_pdfs(["file1.pdf", "file2.pdf"], "merged.pdf")

# Remove specific pages
remove_pdf_pages("document.pdf", pages_to_remove="1,3,5-7", output="cleaned.pdf")
```

### Convert PDF to Images

```python
from pdftools.pdfpages2images import PDF2ImageConverter

converter = PDF2ImageConverter()
converter.process_pdf("document.pdf", output_directory="images")
```

## Module Overview

### Core Modules

#### pdftext_utils.py
Main PDF text extraction and utility functions:
- `extract_and_clean()` - Extract and clean text from PDF
- `clean_page_text()` - Remove artifacts from page text
- `remove_references()` - Remove bibliography sections
- `save_content_to_file()` - Save extracted content to file

#### discard_tracker.py
Track and report on removed content:
- `DiscardTracker` - Main tracking class
- `DiscardedItem` - Represents a discarded item
- `DiscardType` - Enum of removal types

### Extraction Modules

#### count_words.py
Count words in PDF files with page range support

#### extract_sentences.py
Extract individual sentences with page tracking

#### extract_paragraphs.py
Extract paragraphs with section detection

#### extract_book_chapter.py
Advanced chapter extraction with title detection

### PDF Operations

#### split_pdf_file.py
Split large PDFs into smaller files

#### merge_pdfs.py
Merge multiple PDFs into one

#### remove_pdf_pages.py
Remove specific pages from PDFs

#### pdf2text.py
Simple PDF to text conversion

#### pdfpages2images.py
Convert PDF pages to image files

#### pdf_highlighter.py
Highlight text in PDF documents

### Visualization

#### sl_pdfviewer.py
Streamlit-based interactive PDF viewer with search and zoom capabilities

## Testing

### Run All Tests
```bash
make test
```

### Run Specific Test File
```bash
pytest tests/test_count_words.py -v
pytest tests/test_discard_tracker.py -v
pytest tests/test_pdftext_utils.py -v
pytest tests/test_pdf2text.py -v
```

### Test Coverage
- **210 total passing tests**
- **Real PDF file testing** - Tests use actual PDF files (local data directory)
- **Extensive library function coverage**
  - 20 tests for count_words module
  - 19 tests for discard_tracker module
  - 53 tests for pdftext_utils module
  - 15 tests for pdf2text module
  - 14 tests for extract_book_chapter module
  - 15 tests for extract_paragraphs module
  - 18 tests for extract_sentences module
  - 9 tests for merge_pdfs module
  - 12 tests for split_pdf_file module
  - 8 tests for remove_pdf_pages module
  - 16 tests for pdfpages2images module
  - 11 tests for sl_pdfviewer module (under maintenance)

## Project Structure

```
PDFTools/
├── pdftools/                    # Main package
│   ├── pdftext_utils.py        # Core extraction utilities
│   ├── discard_tracker.py      # Content tracking system
│   ├── count_words.py          # Word counting utility
│   ├── extract_sentences.py    # Sentence extraction
│   ├── extract_paragraphs.py   # Paragraph extraction
│   ├── extract_book_chapter.py # Chapter extraction
│   ├── split_pdf_file.py       # PDF splitting
│   ├── merge_pdfs.py           # PDF merging
│   ├── remove_pdf_pages.py     # Page removal
│   ├── pdf2text.py             # PDF to text
│   ├── pdfpages2images.py      # PDF to images
│   ├── pdf_highlighter.py      # PDF highlighting
│   └── sl_pdfviewer.py         # Streamlit viewer
│
├── tests/                       # Test suite
│   ├── conftest.py            # Pytest configuration & fixtures
│   ├── test_count_words.py
│   ├── test_discard_tracker.py
│   ├── test_pdftext_utils.py
│   ├── test_pdf2text.py
│   ├── test_extract_book_chapter.py
│   ├── test_extract_paragraphs.py
│   ├── test_extract_sentences.py
│   ├── test_merge_pdfs.py
│   ├── test_split_pdf_file.py
│   ├── test_remove_pdf_pages.py
│   └── test_pdfpages2images.py
│
├── data/                        # Sample PDF files (ignored by git)
├── docs/                        # Documentation
├── requirements.txt            # Dependencies
├── pyproject.toml             # Project config
├── Makefile                   # Development tasks
└── README.md                  # This file
```

## Configuration

### Discard Types
The tracker recognizes these discard types:
- `PAGE_NUMBER` - Standalone page numbers
- `HEADER_FOOTER` - Headers and footers
- `ARXIV_METADATA` - arXiv metadata
- `DATE_FOOTER` - Date footers
- `SEPARATOR_LINE` - Divider lines
- `SHORT_LINE` - Lines too short to be meaningful
- `REFERENCES_SECTION` - Bibliography sections
- `BIBLIOGRAPHY_ENTRY` - Individual references
- `OTHER` - Other discarded content

## Development

### Create Virtual Environment
```bash
python -m venv pdfenv
source pdfenv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
pip install -e .
```

### Run Tests
```bash
make test
```

## Code Quality

### Recent Improvements (2026-02-09)
- **194 passing tests**
- **Real PDF file testing**
- **Added PDF Highlighter** - Programmatic text highlighting
- **Added Streamlit Viewer** - Interactive PDF exploration
- **Improved Project Structure** - All modules consolidated in `pdftools/`
- **Data Privacy** - `data/` folder now ignored by version control

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Changelog

### Version 2.2.0 (2026-02-09) - Latest
- ✅ **PDF Highlighter** - New module for text highlighting
- ✅ **Streamlit Viewer** - Consolidated interactive viewer in `pdftools/`
- ✅ **Data Ignored** - Excluded `data/` directory from version control
- ✅ **Improved README** - Updated features and usage examples

### Version 2.1.0 (2025-12-06)
- ✅ **Expanded test suite** - 211 passing tests
- ✅ **Real PDF testing** - Replaced all mocks with actual PDF files
- ✅ **Streamlit app** - Added interactive web-based PDF viewer

## Troubleshooting

### ImportError: No module named 'pdftools'
Make sure you're in the correct directory and the package is installed:
```bash
cd PDFTools
pip install -e .
```

---

**Last Updated:** 2026-02-09
**Current Version:** 2.2.0
**Repository:** https://github.com/csv610/PDFTools
**Python Version:** 3.8+
**Status:** ✅ 210 tests passing
