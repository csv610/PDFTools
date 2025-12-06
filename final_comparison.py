import os

print("=" * 90)
print("SUMMARY: PDF Extraction Tools Comparison")
print("=" * 90)

print("\n📊 EXTRACTION RESULTS FOR paper.pdf:")
print("-" * 90)

results = {
    "extract_sentences.py": {
        "file": "extracted_sentences.txt",
        "description": "Sentences (original)"
    },
    "extract_sentences_clean.py": {
        "file": "extracted_sentences_clean.txt",
        "description": "Sentences (cleaned)"
    },
    "extract_paragraphs.py": {
        "file": "extracted_paragraphs.txt",
        "description": "Paragraphs (original)"
    },
    "extract_paragraphs_clean.py": {
        "file": "extracted_paragraphs_clean.txt",
        "description": "Paragraphs (cleaned)"
    }
}

for script, info in results.items():
    if os.path.exists(info["file"]):
        size = os.path.getsize(info["file"]) / 1024  # KB
        # Count items
        with open(info["file"], 'r') as f:
            content = f.read()
            count = content.count("- Page")
        print(f"✓ {script:<30} → {count:3d} items  ({size:6.1f} KB)")
    else:
        print(f"✗ {script:<30} → NOT FOUND")

print("\n" + "=" * 90)
print("KEY IMPROVEMENTS IN CLEAN VERSIONS:")
print("=" * 90)
print("""
✅ REMOVES:
   • Page numbers (standalone digits)
   • arXiv metadata headers/footers
   • Date-only footer lines
   • Symbol separators and dividers
   • Very short line artifacts

✅ PRESERVES:
   • Proper text spacing and formatting
   • Multi-line content (abstracts, author info)
   • Content integrity and structure
   • Accurate page tracking
   • Sentence/paragraph boundaries

📝 USAGE:
   Sentences (clean):   python extract_sentences_clean.py paper.pdf -d
   Paragraphs (clean):  python extract_paragraphs_clean.py paper.pdf -d
""")

print("=" * 90)
