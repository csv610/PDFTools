import os
import re

print("=" * 100)
print("COMPLETE COMPARISON: All Extraction Versions")
print("=" * 100)

extraction_tools = {
    "📄 SENTENCES": {
        "original": ("extracted_sentences.txt", "Original (with refs)"),
        "clean": ("extracted_sentences_clean.txt", "Clean (no headers)"),
        "no_refs": ("extracted_sentences_no_refs.txt", "No References"),
    },
    "📋 PARAGRAPHS": {
        "original": ("extracted_paragraphs.txt", "Original (with refs)"),
        "clean": ("extracted_paragraphs_clean.txt", "Clean (no headers)"),
        "no_refs": ("extracted_paragraphs_no_refs.txt", "No References"),
    }
}

print("\n")

for category, versions in extraction_tools.items():
    print(f"\n{category}")
    print("-" * 100)
    
    for version_name, (filename, description) in versions.items():
        if os.path.exists(filename):
            size = os.path.getsize(filename) / 1024  # KB
            with open(filename, 'r') as f:
                content = f.read()
                count = content.count("- Page")
            print(f"  {description:<30} → {count:3d} items  ({size:6.1f} KB)")
        else:
            print(f"  {description:<30} → NOT FOUND")

print("\n" + "=" * 100)
print("KEY METRICS:")
print("=" * 100)

# Calculate reductions
files_with_refs = {
    "sentences": ("extracted_sentences_clean.txt", "extracted_sentences_no_refs.txt"),
    "paragraphs": ("extracted_paragraphs_clean.txt", "extracted_paragraphs_no_refs.txt"),
}

for item_type, (with_refs, without_refs) in files_with_refs.items():
    if os.path.exists(with_refs) and os.path.exists(without_refs):
        with open(with_refs, 'r') as f:
            count_with = f.read().count("- Page")
        with open(without_refs, 'r') as f:
            count_without = f.read().count("- Page")
        
        reduction = count_with - count_without
        percent = (reduction / count_with) * 100 if count_with > 0 else 0
        
        print(f"\n{item_type.upper()}:")
        print(f"  With references:    {count_with:3d} items")
        print(f"  Without references: {count_without:3d} items")
        print(f"  Removed:            {reduction:3d} items ({percent:.1f}%)")

print("\n" + "=" * 100)
print("AVAILABLE SCRIPTS:\n")

scripts = [
    ("extract_sentences.py", "Basic sentence extraction"),
    ("extract_sentences_clean.py", "Clean sentences (no headers/footers)"),
    ("extract_sentences_no_refs.py", "Clean sentences without references ✨"),
    ("extract_paragraphs.py", "Basic paragraph extraction"),
    ("extract_paragraphs_clean.py", "Clean paragraphs (no headers/footers)"),
    ("extract_paragraphs_no_refs.py", "Clean paragraphs without references ✨"),
]

for script, desc in scripts:
    if os.path.exists(script):
        print(f"✓ {script:<35} {desc}")
    else:
        print(f"✗ {script:<35} {desc}")

print("\n" + "=" * 100)

