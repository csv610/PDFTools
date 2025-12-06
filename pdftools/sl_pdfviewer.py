import streamlit as st
import fitz
from dataclasses import dataclass
from typing import List, Tuple, BinaryIO
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SearchResult:
    """Data class for search results"""
    page_num: int
    matches: List[fitz.Rect]

class PDFState:
    """Class to manage PDF viewer state"""
    def __init__(self):
        if "page_num" not in st.session_state:
            self.init_state()
    
    def init_state(self):
        """Initialize all session state variables"""
        st.session_state.page_num = 0
        st.session_state.pdf_file = None
        st.session_state.doc = None
        st.session_state.annotated_doc = None
        st.session_state.zoom_level = 100
        st.session_state.rotation = 0
        st.session_state.view_mode = "Single Page"
        st.session_state.dpi = 100
        st.session_state.search_results = []
        st.session_state.night_mode = False
        st.session_state.last_query = ""
        st.session_state.highlighted_pages = set()
        st.session_state.search_performed = False

    @property
    def current_page(self) -> int:
        return st.session_state.page_num
    
    @current_page.setter
    def current_page(self, value: int):
        st.session_state.page_num = value

class PDFDocument:
    """Class to handle PDF document operations"""
    def __init__(self, state: PDFState):
        self.state = state
        
    def load_document(self, file_content: bytes) -> None:
        """Load a PDF document from bytes"""
        try:
            self.close_document()
            st.session_state.pdf_file = file_content
            st.session_state.doc = fitz.open(stream=file_content, filetype="pdf")
            st.session_state.annotated_doc = fitz.open(stream=file_content, filetype="pdf")
            self.state.current_page = 0
            logger.info("PDF document loaded successfully")
        except Exception as e:
            logger.error(f"Error loading PDF: {e}")
            raise

    def close_document(self) -> None:
        """Close the current document and clean up"""
        try:
            if st.session_state.doc:
                st.session_state.doc.close()
            if st.session_state.annotated_doc:
                st.session_state.annotated_doc.close()
            st.session_state.doc = None
            st.session_state.annotated_doc = None
            st.session_state.search_performed = False
            st.session_state.search_results = []
            st.session_state.last_query = ""
            st.session_state.highlighted_pages = set()
        except Exception as e:
            logger.error(f"Error closing document: {e}")
            raise

    def render_page(self, page_num: int) -> Tuple[bytes, int, int]:
        """Render a single page"""
        try:
            doc = st.session_state.annotated_doc
            page = doc[page_num]
            
            # Create zoom matrix
            zoom_matrix = fitz.Matrix(st.session_state.zoom_level / 100, 
                                    st.session_state.zoom_level / 100)
            
            # Apply DPI scaling
            dpi_scale = st.session_state.dpi / 72
            zoom_matrix = zoom_matrix * dpi_scale

            # Apply rotation
            if st.session_state.rotation != 0:
                zoom_matrix.prerotate(st.session_state.rotation)
                
            # Re-apply highlights if necessary
            if (page_num in st.session_state.highlighted_pages and 
                st.session_state.last_query):
                self._apply_highlights(page)
            
            # Render page
            pix = page.get_pixmap(matrix=zoom_matrix)
            
            # Apply night mode if enabled
            if st.session_state.night_mode:
                pix.invert_irect(pix.irect)
                
            return pix.tobytes("png"), pix.width, pix.height
        except Exception as e:
            logger.error(f"Error rendering page {page_num}: {e}")
            raise

    def _apply_highlights(self, page: fitz.Page) -> None:
        """Apply search highlights to a page"""
        matches = page.search_for(st.session_state.last_query)
        for rect in matches:
            page.draw_rect(rect, color=(1, 0, 0), width=2)

class SearchManager:
    """Class to handle search operations"""
    def __init__(self, state: PDFState):
        self.state = state

    def search(self, query: str) -> None:
        """Perform search across the document"""
        try:
            doc = st.session_state.annotated_doc
            results = []
            st.session_state.highlighted_pages.clear()
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                matches = page.search_for(query)
                if matches:
                    for rect in matches:
                        page.draw_rect(rect, color=(1, 0, 0), width=2)
                    results.append(SearchResult(page_num, matches))
                    st.session_state.highlighted_pages.add(page_num)
            
            st.session_state.search_results = results
            st.session_state.last_query = query
            st.session_state.search_performed = True
            
        except Exception as e:
            logger.error(f"Error during search: {e}")
            raise

class PDFViewerUI:
    """Class to handle UI components"""
    def __init__(self, state: PDFState, doc_handler: PDFDocument, search_manager: SearchManager):
        self.state = state
        self.doc_handler = doc_handler
        self.search_manager = search_manager

    def render_sidebar(self) -> None:
        """Render sidebar controls"""
        st.sidebar.title("PDF Viewer Controls")
        
        # Display settings
        st.session_state.night_mode = st.sidebar.checkbox("Night Mode", 
                                                         value=st.session_state.night_mode)
        st.session_state.dpi = st.sidebar.number_input("Set DPI (Resolution)", 
                                                      min_value=50, max_value=2400,
                                                      value=st.session_state.dpi, step=50)
        
        # File upload
        uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file and st.session_state.pdf_file != uploaded_file.getvalue():
            self.doc_handler.load_document(uploaded_file.getvalue())

        if not st.session_state.doc:
            return

        # View controls
        self._render_view_controls()
        
        # Navigation controls
        self._render_navigation_controls()
        
        # Search controls
        self._render_search_controls()

    def _render_view_controls(self) -> None:
        """Render view mode and zoom controls"""
        st.sidebar.header("Display Settings")
        st.session_state.view_mode = st.sidebar.radio("View Mode",
                                                     ["Single Page", "Double Page"],
                                                     horizontal=True)
        st.session_state.zoom_level = st.sidebar.slider("Zoom Level (%)",
                                                       min_value=50, max_value=1000,
                                                       value=st.session_state.zoom_level)
        st.session_state.rotation = st.sidebar.selectbox("Rotation",
                                                        options=[0, 90, 180, 270],
                                                        index=[0, 90, 180, 270].index(st.session_state.rotation))

    def _render_navigation_controls(self) -> None:
        """Render page navigation controls"""
        st.sidebar.header("Navigation")
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if st.button("⬅️ Previous", use_container_width=True):
                self._handle_prev_page()
                
        with col2:
            if st.button("Next ➡️", use_container_width=True):
                self._handle_next_page()

        total_pages = st.session_state.doc.page_count
        st.sidebar.number_input("Go to page",
                              min_value=1,
                              max_value=total_pages,
                              value=self.state.current_page + 1,
                              key="target_page",
                              on_change=self._handle_page_jump)

    def _render_search_controls(self) -> None:
        """Render search controls and results"""
        st.sidebar.header("Search")
        search_query = st.sidebar.text_input("Search Text", 
                                           value=st.session_state.last_query)
        search_pressed = st.sidebar.button("Search")

        if search_query and (search_pressed or search_query != st.session_state.last_query):
            self.search_manager.search(search_query)

        if st.session_state.search_performed:
            self._display_search_results()

    def _display_search_results(self) -> None:
        """Display search results in sidebar"""
        if st.session_state.search_results:
            st.sidebar.write(f"Found {len(st.session_state.search_results)} page(s) with matches.")
            for result in st.session_state.search_results:
                st.sidebar.write(f"Page {result.page_num + 1}: {len(result.matches)} match(es)")
        else:
            st.sidebar.write("No matches found.")

    def render_main_view(self) -> None:
        """Render the main PDF view"""
        if not st.session_state.doc:
            self._render_welcome_message()
            return

        try:
            if st.session_state.view_mode == "Double Page":
                self._render_double_page_view()
            else:
                self._render_single_page_view()
        except Exception as e:
            st.error(f"Error displaying PDF: {str(e)}")

    def _render_single_page_view(self) -> None:
        """Render single page view"""
        image_bytes, width, height = self.doc_handler.render_page(self.state.current_page)
        st.image(image_bytes, use_container_width=True)

    def _render_double_page_view(self) -> None:
        """Render double page view"""
        col1, col2 = st.columns(2)
        
        with col1:
            image_bytes, width, height = self.doc_handler.render_page(self.state.current_page)
            st.image(image_bytes, use_container_width=True)
        
        next_page = self.state.current_page + 1
        if next_page < st.session_state.doc.page_count:
            with col2:
                image_bytes, width, height = self.doc_handler.render_page(next_page)
                st.image(image_bytes, use_container_width=True)
        else:
            with col2:
                st.write("No more pages to display.")

    def _render_welcome_message(self) -> None:
        """Render welcome message when no document is loaded"""
        st.write("Please upload a PDF file")
        st.markdown("""
        ### Features Available:
        - Single and double page viewing modes
        - Zoom control (50% - 1000%)
        - Page rotation (0°, 90°, 180°, 270°)
        - Direct page navigation
        - Previous/Next navigation
        - Text search with highlights
        - Night mode for comfortable reading
        - Download annotated PDF
        """)

    def _handle_next_page(self) -> None:
        """Handle next page navigation"""
        doc = st.session_state.doc
        increment = 2 if st.session_state.view_mode == "Double Page" else 1
        if self.state.current_page < doc.page_count - increment:
            self.state.current_page += increment

    def _handle_prev_page(self) -> None:
        """Handle previous page navigation"""
        decrement = 2 if st.session_state.view_mode == "Double Page" else 1
        if self.state.current_page >= decrement:
            self.state.current_page -= decrement

    def _handle_page_jump(self) -> None:
        """Handle direct page navigation"""
        if st.session_state.target_page > 0:
            doc = st.session_state.doc
            if st.session_state.target_page <= doc.page_count:
                self.state.current_page = st.session_state.target_page - 1

def main():
    # Set up page config
    st.set_page_config(layout="wide", page_title="PDF Viewer")
    
    try:
        # Initialize components
        state = PDFState()
        doc_handler = PDFDocument(state)
        search_manager = SearchManager(state)
        ui = PDFViewerUI(state, doc_handler, search_manager)
        
        # Render UI
        ui.render_sidebar()
        ui.render_main_view()
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error("An error occurred. Please try again or contact support.")

if __name__ == "__main__":
    main()
