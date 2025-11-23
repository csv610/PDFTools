# Contributing to PDFTools

Thank you for your interest in contributing to PDFTools! We welcome all contributions, whether they're bug reports, feature requests, or code improvements.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/PDFTools.git
   cd PDFTools
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install black flake8 isort pytest pytest-cov
   ```

## Development Workflow

1. Create a branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and test them:
   ```bash
   # Run linting
   flake8 .
   black .
   isort .

   # Run tests if available
   pytest tests/ -v
   ```

3. Commit with a clear message:
   ```bash
   git commit -m "Add clear description of changes"
   ```

4. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

5. Open a Pull Request on GitHub

## Code Style

We follow PEP 8 with some specific conventions:

- Use `black` for code formatting (default settings)
- Use `isort` for import sorting
- Maximum line length: 127 characters
- Type hints are encouraged for new functions

Format your code before committing:
```bash
black .
isort .
```

## Reporting Issues

When reporting a bug, please include:

- Python version
- Operating system
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Any error messages or logs

## Pull Request Guidelines

- Keep PRs focused on a single feature or fix
- Update documentation if needed
- Add tests for new functionality
- Reference any related issues

## Project Structure

```
PDFTools/
├── pdf2text.py              # Text extraction
├── count_words.py           # Word counting
├── split_pdf_file.py        # PDF splitting
├── remove_pdf_pages.py      # Page removal
├── pdfpages2images.py       # PDF to image conversion
├── merge_pdfs.py            # PDF merging
├── requirements.txt         # Dependencies
├── README.md               # Documentation
├── LICENSE                 # MIT License
└── .github/
    └── workflows/
        └── tests.yml       # CI/CD pipeline
```

## Testing

While full test coverage is being developed, you can test functionality manually:

```bash
# Test pdf2text
python pdf2text.py sample.pdf

# Test count_words
python count_words.py -i sample.pdf -v

# Test split_pdf
python split_pdf_file.py -i sample.pdf -p 10

# Test remove_pages
python remove_pdf_pages.py -i sample.pdf -o output.pdf -p 1,3

# Test image conversion
python pdfpages2images.py sample.pdf
```

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

Thank you for contributing!
