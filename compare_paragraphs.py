import re

print("=" * 80)
print("COMPARISON: Original vs Clean Paragraph Extraction")
print("=" * 80)

# Check original file
with open('extracted_paragraphs.txt', 'r', encoding='utf-8') as f:
    original_content = f.read()
original_multi_page = len(re.findall(r'\[Paragraph \d+ - Pages \d+-\d+\]', original_content))
original_count = len(re.findall(r'\[Paragraph \d+ - Page', original_content))

# Extract paragraph content from original
original_para_matches = re.findall(r'\[Paragraph \d+ - Pages? [\d\-]+\]\n(.*?)\n={80}', original_content, re.DOTALL)

# Check clean file
with open('extracted_paragraphs_clean.txt', 'r', encoding='utf-8') as f:
    clean_content = f.read()
clean_multi_page = len(re.findall(r'\[Paragraph \d+ - Pages \d+-\d+\]', clean_content))
clean_count = len(re.findall(r'\[Paragraph \d+ - Page', clean_content))

# Extract paragraph content from clean
clean_para_matches = re.findall(r'\[Paragraph \d+ - Pages? [\d\-]+\]\n(.*?)\n={80}', clean_content, re.DOTALL)

print(f"\nOriginal extraction:")
print(f"  Total paragraphs: {original_count}")
print(f"  Multi-page paragraphs: {original_multi_page}")
print(f"  Single-page paragraphs: {original_count - original_multi_page}")
print(f"  Total characters: {sum(len(p) for p in original_para_matches):,}")

print(f"\nClean extraction (with page number/header removal):")
print(f"  Total paragraphs: {clean_count}")
print(f"  Multi-page paragraphs: {clean_multi_page}")
print(f"  Single-page paragraphs: {clean_count - clean_multi_page}")
print(f"  Total characters: {sum(len(p) for p in clean_para_matches):,}")

print(f"\nImpact of cleaning:")
print(f"  Character difference: {sum(len(p) for p in clean_para_matches) - sum(len(p) for p in original_para_matches):,}")
print(f"  Multi-page change: {clean_multi_page - original_multi_page}")

# Show first paragraph from each
print("\n" + "=" * 80)
print("FIRST PARAGRAPH - Original:")
print("=" * 80)
print(original_para_matches[0][:300] + "...")

print("\n" + "=" * 80)
print("FIRST PARAGRAPH - Clean:")
print("=" * 80)
print(clean_para_matches[0][:300] + "...")
