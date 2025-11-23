from PyPDF2 import PdfMerger

def merge_pdfs(input_files, output_file):
    merger = PdfMerger()
    
    for file in input_files:
        merger.append(file)
    
    merger.write(output_file)
    merger.close()

# Usage example
input_files = ["file1.pdf", "file2.pdf", "file3.pdf"]
output_file = "merged.pdf"
merge_pdfs(input_files, output_file)
