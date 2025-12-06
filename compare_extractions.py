import re

print("=" * 80)
print("COMPARISON: Original vs Clean Extraction")
print("=" * 80)

# Check original file
with open('extracted_sentences.txt', 'r', encoding='utf-8') as f:
    original_content = f.read()
original_multi_page = len(re.findall(r'\[Sentence \d+ - Pages \d+-\d+\]', original_content))
original_count = len(re.findall(r'\[Sentence \d+ - Page', original_content))

# Check clean file
with open('extracted_sentences_clean.txt', 'r', encoding='utf-8') as f:
    clean_content = f.read()
clean_multi_page = len(re.findall(r'\[Sentence \d+ - Pages \d+-\d+\]', clean_content))
clean_count = len(re.findall(r'\[Sentence \d+ - Page', clean_content))

print(f"\nOriginal extraction:")
print(f"  Total sentences: {original_count}")
print(f"  Multi-page sentences: {original_multi_page}")
print(f"  Single-page sentences: {original_count - original_multi_page}")

print(f"\nClean extraction (with page number/header removal):")
print(f"  Total sentences: {clean_count}")
print(f"  Multi-page sentences: {clean_multi_page}")
print(f"  Single-page sentences: {clean_count - clean_multi_page}")

print(f"\nImprovement:")
print(f"  Removed artifacts: {original_count - clean_count} sentences")
print(f"  Reduced multi-page sentences: {original_multi_page - clean_multi_page}")
