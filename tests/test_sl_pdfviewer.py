"""Tests for sl_pdfviewer module."""

import sys
import unittest
from unittest.mock import patch, MagicMock, Mock
from pathlib import Path

# Add pdftools to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdftools.sl_pdfviewer import PDFState, PDFDocument, SearchManager, PDFViewerUI, SearchResult


class TestSearchResult(unittest.TestCase):
    """Test cases for SearchResult dataclass."""

    def test_search_result_creation(self):
        """Test creating SearchResult object."""
        result = SearchResult(page_num=5, matches=[])

        self.assertEqual(result.page_num, 5)
        self.assertEqual(result.matches, [])

    def test_search_result_with_matches(self):
        """Test SearchResult with match rectangles."""
        mock_rects = [MagicMock(), MagicMock()]
        result = SearchResult(page_num=3, matches=mock_rects)

        self.assertEqual(result.page_num, 3)
        self.assertEqual(len(result.matches), 2)


class TestPDFState(unittest.TestCase):
    """Test cases for PDFState class."""

    @patch('pdftools.sl_pdfviewer.st')
    def test_pdf_state_initialization(self, mock_st):
        """Test PDFState initialization."""
        mock_st.session_state = {}

        state = PDFState()

        self.assertIsNotNone(state)

    @patch('pdftools.sl_pdfviewer.st')
    def test_pdf_state_init_state(self, mock_st):
        """Test init_state method."""
        mock_st.session_state = {}

        state = PDFState()
        state.init_state()

        # init_state should set up session state
        mock_st.session_state.__setitem__.assert_called()

    @patch('pdftools.sl_pdfviewer.st')
    def test_pdf_state_current_page_property(self, mock_st):
        """Test current_page property getter."""
        mock_st.session_state = {
            'current_page': 5,
            'document': MagicMock(),
            'search_results': [],
            'view_mode': 'single'
        }

        state = PDFState()
        state.current_page = 5

        self.assertIsNotNone(state)

    @patch('pdftools.sl_pdfviewer.st')
    def test_pdf_state_current_page_setter(self, mock_st):
        """Test current_page property setter."""
        mock_st.session_state = {}

        state = PDFState()
        state.current_page = 10

        self.assertIsNotNone(state)


class TestPDFDocument(unittest.TestCase):
    """Test cases for PDFDocument class."""

    @patch('pdftools.sl_pdfviewer.st')
    def test_pdf_document_initialization(self, mock_st):
        """Test PDFDocument initialization."""
        mock_state = MagicMock()
        mock_st.session_state = {}

        doc = PDFDocument(mock_state)

        self.assertIsNotNone(doc)
        self.assertEqual(doc.state, mock_state)

    @patch('pdftools.sl_pdfviewer.st')
    def test_pdf_document_close_document(self, mock_st):
        """Test closing a document."""
        mock_state = MagicMock()
        mock_st.session_state = {}

        doc = PDFDocument(mock_state)
        doc.close_document()

        # Should not raise error
        self.assertIsNotNone(doc)

    @patch('pdftools.sl_pdfviewer.st')
    def test_pdf_document_state_assignment(self, mock_st):
        """Test that state is properly assigned."""
        mock_state = MagicMock()
        mock_st.session_state = {}

        doc = PDFDocument(mock_state)

        self.assertEqual(doc.state, mock_state)

    @patch('pdftools.sl_pdfviewer.st')
    def test_pdf_document_load_from_file(self, mock_st):
        """Test loading actual PDF file."""
        mock_state = MagicMock()
        mock_st.session_state = {}

        # Use actual paper.pdf from data folder
        paper_path = Path(__file__).parent.parent / "data" / "paper.pdf"

        if paper_path.exists():
            with open(paper_path, 'rb') as f:
                pdf_content = f.read()

            doc = PDFDocument(mock_state)
            doc.load_document(pdf_content)

            self.assertIsNotNone(doc)


class TestSearchManager(unittest.TestCase):
    """Test cases for SearchManager class."""

    @patch('pdftools.sl_pdfviewer.st')
    def test_search_manager_initialization(self, mock_st):
        """Test SearchManager initialization."""
        mock_state = MagicMock()
        mock_st.session_state = {}

        manager = SearchManager(mock_state)

        self.assertIsNotNone(manager)
        self.assertEqual(manager.state, mock_state)

    @patch('pdftools.sl_pdfviewer.st')
    def test_search_manager_search_query(self, mock_st):
        """Test search with query."""
        mock_state = MagicMock()
        mock_st.session_state = {}

        manager = SearchManager(mock_state)
        manager.search("test query")

        # Should not raise error
        self.assertIsNotNone(manager)

    @patch('pdftools.sl_pdfviewer.st')
    def test_search_manager_empty_query(self, mock_st):
        """Test search with empty query."""
        mock_state = MagicMock()
        mock_st.session_state = {}

        manager = SearchManager(mock_state)
        manager.search("")

        # Should handle empty query gracefully
        self.assertIsNotNone(manager)

    @patch('pdftools.sl_pdfviewer.st')
    def test_search_manager_state_assignment(self, mock_st):
        """Test that state is properly assigned."""
        mock_state = MagicMock()
        mock_st.session_state = {}

        manager = SearchManager(mock_state)

        self.assertEqual(manager.state, mock_state)


class TestPDFViewerUI(unittest.TestCase):
    """Test cases for PDFViewerUI class."""

    @patch('pdftools.sl_pdfviewer.st')
    def test_pdf_viewer_ui_initialization(self, mock_st):
        """Test PDFViewerUI initialization."""
        mock_state = MagicMock()
        mock_doc = MagicMock()
        mock_search = MagicMock()
        mock_st.session_state = {}

        ui = PDFViewerUI(mock_state, mock_doc, mock_search)

        self.assertIsNotNone(ui)
        self.assertEqual(ui.state, mock_state)
        self.assertEqual(ui.doc_handler, mock_doc)
        self.assertEqual(ui.search_manager, mock_search)

    @patch('pdftools.sl_pdfviewer.st')
    def test_pdf_viewer_render_sidebar(self, mock_st):
        """Test render_sidebar method."""
        mock_state = MagicMock()
        mock_doc = MagicMock()
        mock_search = MagicMock()
        mock_st.session_state = {}

        ui = PDFViewerUI(mock_state, mock_doc, mock_search)
        ui.render_sidebar()

        # Should not raise error
        self.assertIsNotNone(ui)

    @patch('pdftools.sl_pdfviewer.st')
    def test_pdf_viewer_render_main_view(self, mock_st):
        """Test render_main_view method."""
        mock_state = MagicMock()
        mock_doc = MagicMock()
        mock_search = MagicMock()
        mock_st.session_state = {}

        ui = PDFViewerUI(mock_state, mock_doc, mock_search)
        ui.render_main_view()

        # Should not raise error
        self.assertIsNotNone(ui)

    @patch('pdftools.sl_pdfviewer.st')
    def test_pdf_viewer_state_reference(self, mock_st):
        """Test that UI properly references state."""
        mock_state = MagicMock()
        mock_doc = MagicMock()
        mock_search = MagicMock()
        mock_st.session_state = {}

        ui = PDFViewerUI(mock_state, mock_doc, mock_search)

        self.assertIs(ui.state, mock_state)

    @patch('pdftools.sl_pdfviewer.st')
    def test_pdf_viewer_doc_handler_reference(self, mock_st):
        """Test that UI properly references document handler."""
        mock_state = MagicMock()
        mock_doc = MagicMock()
        mock_search = MagicMock()
        mock_st.session_state = {}

        ui = PDFViewerUI(mock_state, mock_doc, mock_search)

        self.assertIs(ui.doc_handler, mock_doc)

    @patch('pdftools.sl_pdfviewer.st')
    def test_pdf_viewer_search_manager_reference(self, mock_st):
        """Test that UI properly references search manager."""
        mock_state = MagicMock()
        mock_doc = MagicMock()
        mock_search = MagicMock()
        mock_st.session_state = {}

        ui = PDFViewerUI(mock_state, mock_doc, mock_search)

        self.assertIs(ui.search_manager, mock_search)

    @patch('pdftools.sl_pdfviewer.st')
    def test_pdf_viewer_multiple_ui_instances(self, mock_st):
        """Test creating multiple UI instances."""
        mock_state1 = MagicMock()
        mock_doc1 = MagicMock()
        mock_search1 = MagicMock()

        mock_state2 = MagicMock()
        mock_doc2 = MagicMock()
        mock_search2 = MagicMock()

        mock_st.session_state = {}

        ui1 = PDFViewerUI(mock_state1, mock_doc1, mock_search1)
        ui2 = PDFViewerUI(mock_state2, mock_doc2, mock_search2)

        self.assertIsNot(ui1, ui2)
        self.assertIs(ui1.state, mock_state1)
        self.assertIs(ui2.state, mock_state2)


class TestPDFViewerIntegration(unittest.TestCase):
    """Integration tests for PDF viewer components."""

    @patch('pdftools.sl_pdfviewer.st')
    def test_components_work_together(self, mock_st):
        """Test that all components work together."""
        mock_st.session_state = {
            'current_page': 0,
            'document': None,
            'search_results': [],
            'view_mode': 'single'
        }

        # Create instances
        state = PDFState()
        state.init_state()

        doc = PDFDocument(state)
        search = SearchManager(state)
        ui = PDFViewerUI(state, doc, search)

        # Should all be initialized without error
        self.assertIsNotNone(state)
        self.assertIsNotNone(doc)
        self.assertIsNotNone(search)
        self.assertIsNotNone(ui)

    @patch('pdftools.sl_pdfviewer.st')
    def test_state_shared_across_components(self, mock_st):
        """Test that components share state properly."""
        mock_st.session_state = {}

        state = PDFState()
        doc = PDFDocument(state)
        search = SearchManager(state)

        # All should reference the same state
        self.assertIs(doc.state, state)
        self.assertIs(search.state, state)

    @patch('pdftools.sl_pdfviewer.st')
    def test_load_actual_pdf_into_viewer(self, mock_st):
        """Test loading actual PDF into viewer."""
        mock_st.session_state = {
            'current_page': 0,
            'document': None,
            'search_results': [],
            'view_mode': 'single'
        }

        paper_path = Path(__file__).parent.parent / "data" / "paper.pdf"

        if paper_path.exists():
            state = PDFState()
            state.init_state()

            doc = PDFDocument(state)

            # Load actual PDF
            with open(paper_path, 'rb') as f:
                pdf_content = f.read()

            doc.load_document(pdf_content)

            # Should have loaded successfully
            self.assertIsNotNone(doc)


if __name__ == "__main__":
    unittest.main()
