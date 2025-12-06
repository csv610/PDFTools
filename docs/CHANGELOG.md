# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-23

### Added
- Initial release of PDFTools
- PDF to text extraction (`pdf2text.py`)
  - Extract text from entire PDFs
  - Clean text output
- Word counting tool (`count_words.py`)
  - Count words in complete documents
  - Support for page ranges
  - Verbose logging and detailed output
  - Per-page word count in debug mode
- PDF splitting tool (`split_pdf_file.py`)
  - Split large PDFs into smaller chunks
  - Configurable pages per split
  - Support for page range selection
  - Numbered output files
- Page removal tool (`remove_pdf_pages.py`)
  - Remove specific pages from PDFs
  - Support for single pages and ranges
  - Mixed format support (e.g., "1,3-5,7")
  - Output file specification
- PDF to image conversion (`pdfpages2images.py`)
  - Convert PDF pages to PNG images
  - Configurable DPI resolution
  - Batch processing with chunk size control
  - Progress logging
- PDF merging tool (`merge_pdfs.py`)
  - Merge multiple PDFs into a single file
  - Preserves page structure

### Documentation
- Comprehensive README with usage examples
- CONTRIBUTING.md for developers
- MIT License
- .gitignore for common Python files
- GitHub Actions CI/CD workflow
- requirements.txt with all dependencies

### Quality Assurance
- GitHub Actions workflow for testing across Python 3.8-3.12
- Tests on Ubuntu, macOS, and Windows
- Code quality checks (flake8, black, isort)

## [Unreleased]

### Planned
- Unit test suite
- Python API (not just CLI)
- Support for encrypted PDFs
- Batch processing mode for multiple files
- Configuration file support
- Progress bars for long operations
- More detailed error recovery

---

## How to Use This Project

See [README.md](README.md) for installation and usage instructions.

## Reporting Issues

Found a bug? Please open an [issue](https://github.com/yourusername/PDFTools/issues) with:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
