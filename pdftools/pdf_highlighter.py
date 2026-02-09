import fitz
from typing import List
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Highlighter:
    """Class to highlight specific words in a PDF document"""
    def __init__(self):
        pass

    def highlight_words(self, input_path: str, words: List[str], output_path: str):
        """
        Searches for each word in the list across all pages and 
        adds a light highlight (bounding box) to them.
        """
        try:
            doc = fitz.open(input_path)
            for page in doc:
                for word in words:
                    # search_for returns a list of Rect objects
                    text_instances = page.search_for(word)
                    for inst in text_instances:
                        # add_highlight_annot is the standard way to highlight text in PDFs
                        annot = page.add_highlight_annot(inst)
                        # Optional: set color, default is usually yellow
                        annot.set_colors(stroke=(1.0, 0, 0)) 
                        annot.set_opacity(0.4)
                        annot.update()
            
            doc.save(output_path)
            doc.close()
            logger.info(f"Successfully highlighted words and saved to {output_path}")
        except Exception as e:
            logger.error(f"Error during highlighting: {e}")
            raise

def main():
    parser = argparse.ArgumentParser(description="Highlight words in a PDF file.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input PDF file")
    parser.add_argument("-o", "--output", required=True, help="Path to the output PDF file")
    parser.add_argument("-w", "--words", required=True, nargs="+", help="Words to highlight")
    
    args = parser.parse_args()
    
    highlighter = Highlighter()
    highlighter.highlight_words(args.input, args.words, args.output)

if __name__ == "__main__":
    main()
