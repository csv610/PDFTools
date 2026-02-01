from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from pathlib import Path
from typing import List
from tqdm import tqdm
import sys
import os

class PDF2ImageConverter:
    def __init__(self) -> None:
        """
        Initialize the PDF to Image converter.
        
        This creates a reusable converter that can process multiple PDF files
        with different settings for each conversion.
        """
        self.page_count: int | None = None
        self.image_paths: List[str] = []

    def process_pdf(self, input_file: str, output_directory: str = "images", dpi: int = 300, chunk_size: int = 5) -> List[str]:
        """Process the PDF file: create output directory, get page count, and convert to images.
        
        Args:
            input_file: Path to the input PDF file
            output_directory: Directory where converted images will be saved (default: "images")
            dpi: Resolution in dots per inch (default: 300)
            chunk_size: Number of pages to process at once (default: 5)
            
        Returns:
            List of paths to the generated image files
        """
        self._create_output_directory(output_directory)
        self._get_page_count(input_file)
        image_paths = self._convert_pdf_pages_to_images(input_file, output_directory, dpi, chunk_size)
        return image_paths

    def _create_output_directory(self, output_directory: str) -> None:
        """Create the output directory if it doesn't exist."""
        try:
            Path(output_directory).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise RuntimeError(f"Failed to create output directory: {e}")

    def _get_page_count(self, input_file: str) -> int:
        """Get the total number of pages in the PDF."""
        try:
            with open(input_file, 'rb') as f:
                pdf = PdfReader(f)
                self.page_count = len(pdf.pages)
                return self.page_count
        except Exception as e:
            raise RuntimeError(f"Failed to get page count: {e}")

    def _convert_pdf_pages_to_images(self, input_file: str, output_directory: str, dpi: int = 300, chunk_size: int = 5) -> List[str]:
        """Convert PDF pages to images and save each page to the output directory.
        
        Args:
            input_file: Path to the input PDF file
            output_directory: Directory where converted images will be saved
            dpi: Resolution in dots per inch (default: 300)
            chunk_size: Number of pages to process at once (default: 5)
        """
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        if dpi <= 0:
            raise ValueError(f"DPI must be positive, got {dpi}")
        if chunk_size <= 0:
            raise ValueError(f"Chunk size must be positive, got {chunk_size}")
        
        if self.page_count is None:
            raise RuntimeError("Page count not initialized. Call _get_page_count() first.")

        leading_zeros = len(str(self.page_count))
        total_chunks = (self.page_count + chunk_size - 1) // chunk_size
        
        with tqdm(total=self.page_count, desc="Converting pages", unit="page") as pbar:
            for start_page in range(1, self.page_count + 1, chunk_size):
                end_page = min(start_page + chunk_size - 1, self.page_count)
                try:
                    images = convert_from_path(
                        input_file,
                        dpi=dpi,
                        first_page=start_page,
                        last_page=end_page
                    )
                    for i, image in enumerate(images):
                        page_num = start_page + i
                        output_file = os.path.join(
                            output_directory,
                            f"page_{str(page_num).zfill(leading_zeros)}.png"
                        )
                        self._save_image(image, output_file)
                        self.image_paths.append(output_file)
                        pbar.update(1)
                except Exception as e:
                    raise RuntimeError(f"Failed to convert pages {start_page} to {end_page}: {e}")
        return self.image_paths

    def _save_image(self, image, output_file: str) -> None:
        """Save the image to the specified output file."""
        try:
            image.save(output_file, "PNG")
        except Exception as e:
            raise RuntimeError(f"Failed to save image {output_file}: {e}")

def main() -> None:
    """Main entry point for the PDF to Image converter."""
    if len(sys.argv) != 2:
        print("Usage: python pdfpages2images.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_directory = "images"

    try:
        converter = PDF2ImageConverter()
        image_paths = converter.process_pdf(input_file, output_directory)
        print(f"\nConversion successful! {len(image_paths)} images saved to '{output_directory}/'")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
