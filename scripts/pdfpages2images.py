from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from pathlib import Path
from typing import List
import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class PDF2ImageConverter:
    def __init__(self, input_file: str, output_directory: str, dpi: int = 300, chunk_size: int = 5) -> None:
        """
        Initialize the PDF to Image converter.

        Args:
            input_file: Path to the input PDF file
            output_directory: Directory where converted images will be saved
            dpi: Resolution in dots per inch (default: 300)
            chunk_size: Number of pages to process at once (default: 5)

        Raises:
            FileNotFoundError: If input PDF file does not exist
            ValueError: If dpi or chunk_size are invalid
        """
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        if dpi <= 0:
            raise ValueError(f"DPI must be positive, got {dpi}")
        if chunk_size <= 0:
            raise ValueError(f"Chunk size must be positive, got {chunk_size}")

        self.input_file = input_file
        self.output_directory = output_directory
        self.dpi = dpi
        self.chunk_size = chunk_size
        self.page_count: int | None = None
        self.image_paths: List[str] = []

    def create_output_directory(self) -> None:
        """Create the output directory if it doesn't exist."""
        try:
            Path(self.output_directory).mkdir(parents=True, exist_ok=True)
            logging.info(f"Output directory ready: {self.output_directory}")
        except Exception as e:
            raise RuntimeError(f"Failed to create output directory: {e}")

    def get_page_count(self) -> int:
        """Get the total number of pages in the PDF."""
        try:
            with open(self.input_file, 'rb') as f:
                pdf = PdfReader(f)
                self.page_count = len(pdf.pages)
                logging.info(f"PDF has {self.page_count} pages")
                return self.page_count
        except Exception as e:
            logging.error(f"Error getting page count: {e}")
            raise RuntimeError(f"Failed to get page count: {e}")

    def get_images(self) -> List[str]:
        """Convert PDF to images and save each page to the output directory."""
        if self.page_count is None:
            raise RuntimeError("Page count not initialized. Call get_page_count() first.")

        leading_zeros = len(str(self.page_count))
        for start_page in range(1, self.page_count + 1, self.chunk_size):
            end_page = min(start_page + self.chunk_size - 1, self.page_count)
            try:
                logging.info(f"Converting pages {start_page} to {end_page}...")
                images = convert_from_path(
                    self.input_file,
                    dpi=self.dpi,
                    first_page=start_page,
                    last_page=end_page
                )
                for i, image in enumerate(images):
                    page_num = start_page + i
                    output_file = os.path.join(
                        self.output_directory,
                        f"page_{str(page_num).zfill(leading_zeros)}.png"
                    )
                    self.save_image(image, output_file)
                    self.image_paths.append(output_file)
                    logging.debug(f"Saved: {output_file}")
            except Exception as e:
                logging.error(f"Error converting pages {start_page} to {end_page}: {e}")
                raise RuntimeError(f"Failed to convert pages {start_page} to {end_page}: {e}")
        return self.image_paths

    def save_image(self, image, output_file: str) -> None:
        """Save the image to the specified output file."""
        try:
            image.save(output_file, "PNG")
        except Exception as e:
            logging.error(f"Error saving image {output_file}: {e}")
            raise RuntimeError(f"Failed to save image {output_file}: {e}")

    def convert_to_images(self) -> List[str]:
        """Convert a PDF file to images and save them to the specified output directory."""
        logging.info(f"Starting conversion of {self.input_file}")
        self.create_output_directory()
        self.get_page_count()
        image_paths = self.get_images()
        logging.info(f"Conversion complete. {len(image_paths)} images saved.")
        return image_paths

def main() -> None:
    """Main entry point for the PDF to Image converter."""
    if len(sys.argv) != 2:
        print("Usage: python pdfpages2images.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_directory = "images"

    try:
        converter = PDF2ImageConverter(input_file, output_directory)
        image_paths = converter.convert_to_images()
        print(f"\nConversion successful! {len(image_paths)} images saved to '{output_directory}/'")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
