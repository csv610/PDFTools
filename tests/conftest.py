"""Pytest configuration and fixtures for PDF tools tests."""

import pytest
from pathlib import Path

# Path to test PDFs
TEST_DATA_DIR = Path(__file__).parent.parent / "data"
PAPER_PDF = TEST_DATA_DIR / "paper.pdf"
LARGE_PDF = TEST_DATA_DIR / "536.pdf"


@pytest.fixture
def paper_pdf():
    """Fixture providing path to small test PDF (15 pages)."""
    return str(PAPER_PDF)


@pytest.fixture
def large_pdf():
    """Fixture providing path to large test PDF (442 pages)."""
    return str(LARGE_PDF)


@pytest.fixture
def test_pdfs():
    """Fixture providing both test PDFs."""
    return {
        "small": str(PAPER_PDF),
        "large": str(LARGE_PDF)
    }
