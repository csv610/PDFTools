import PyPDF2
import sys

def pdf_to_text(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text_parts = []
            for page in reader.pages:
                text_parts.append(page.extract_text())
            return '\n\n'.join(text_parts)
    except FileNotFoundError:
        print(f"Error: File '{pdf_path}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error processing PDF: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf2text.py <pdf_file>", file=sys.stderr)
        sys.exit(1)

    extracted_text = pdf_to_text(sys.argv[1])
    print(extracted_text)

