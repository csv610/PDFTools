# PDF Viewer Web App

A Streamlit-based PDF viewer with advanced features for interactive PDF viewing and analysis.

## Features

- **Single and Double Page Viewing**: Switch between single page and book-style double page views
- **Zoom Control**: Adjust zoom level from 50% to 1000%
- **Page Rotation**: Rotate pages (0°, 90°, 180°, 270°)
- **Direct Navigation**: Jump directly to any page
- **Text Search**: Search for text within the PDF and navigate to matching pages
- **Night Mode**: Eye-friendly dark mode for comfortable reading
- **Download**: Export annotated PDFs

## Running the App

### Prerequisites
- Python 3.8+
- Dependencies listed in `/requirements.txt`

### Installation

```bash
# Install dependencies
pip install -e ..

# Or with dev dependencies
pip install -e "..[dev]"
```

### Running the Application

```bash
# From the project root
streamlit run app/app.py

# Or from the app directory
cd app
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Usage

1. **Upload a PDF**: Use the file uploader in the sidebar to load a PDF file
2. **Navigate**: Use Previous/Next buttons or the page number input
3. **Search**: Enter text in the search box to find occurrences within the PDF
4. **Adjust View**: Use controls to change zoom, rotation, and view mode
5. **Download**: Download annotated versions of your PDF

## File Structure

- `app.py`: Main entry point for the Streamlit application
- `viewer.py`: Core PDF viewer classes and UI components
  - `PDFState`: Manages viewer state
  - `PDFDocument`: Handles PDF document operations
  - `SearchManager`: Manages text search functionality
  - `PDFViewerUI`: Renders the UI components

## Architecture

The application uses a modular design:

- **State Management**: `PDFState` maintains session-based state
- **Document Handling**: `PDFDocument` manages PDF rendering and page operations
- **Search Functionality**: `SearchManager` handles text search and highlighting
- **UI Rendering**: `PDFViewerUI` orchestrates the sidebar and main view rendering

## Dependencies

- **streamlit**: Web framework
- **fitz (PyMuPDF)**: PDF rendering and manipulation
- **pypdf**: PDF reading and writing
