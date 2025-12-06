# Quick Setup Guide

Get PDFTools up and running in minutes.

## Option 1: Manual Setup (Recommended)

### 1. Prerequisites
- Python 3.8 or higher installed
- Git installed

### 2. Clone the Repository
```bash
git clone https://github.com/yourusername/PDFTools.git
cd PDFTools
```

### 3. Create Virtual Environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Verify Installation
```bash
# Test pdf2text
python pdf2text.py README.md

# Test count_words
python count_words.py -i README.md

# Test help messages
python split_pdf_file.py --help
python remove_pdf_pages.py --help
```

## Option 2: Using make (if available)

```bash
make setup
make test
```

## System-Specific Notes

### macOS
If you encounter issues with pdf2image:
```bash
brew install poppler
```

### Linux (Ubuntu/Debian)
Install system dependencies:
```bash
sudo apt-get install python3-pip python3-venv
sudo apt-get install poppler-utils  # For pdf2image
```

### Windows
- Use PowerShell or Command Prompt
- Ensure Python is in your PATH
- For pdf2image, install Poppler from: https://github.com/oschwartz10612/poppler-windows/releases

## Next Steps

1. Read the [README.md](README.md) for comprehensive usage guide
2. Check out the [examples](README.md#examples) section
3. Review [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute
4. See [CHANGELOG.md](CHANGELOG.md) for version history

## Troubleshooting

### "No module named 'pypdf'"
```bash
pip install -r requirements.txt
```

### "ImportError: cannot import name 'convert_from_path'"
```bash
pip install pdf2image Pillow
```

### macOS: "Unable to locate poppler"
```bash
brew install poppler
```

### Windows: "Poppler not found"
Download from: https://github.com/oschwartz10612/poppler-windows/releases
And add to PATH or specify explicitly.

## Getting Help

- Check the [README.md](README.md) troubleshooting section
- Review tool help: `python <tool>.py --help`
- Open an issue on GitHub with details about your problem

## Quick Commands Reference

```bash
# Text extraction
python pdf2text.py document.pdf > output.txt

# Word counting
python count_words.py -i document.pdf -v

# PDF splitting
python split_pdf_file.py -i large.pdf -p 20 -d output/

# Page removal
python remove_pdf_pages.py -i input.pdf -o output.pdf -p 1,5,10

# Image conversion
python pdfpages2images.py document.pdf --dpi 300

# Merging
python merge_pdfs.py file1.pdf file2.pdf file3.pdf output.pdf
```

Enjoy using PDFTools!
