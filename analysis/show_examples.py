import re

print("=" * 90)
print("DETAILED EXAMPLES: Special Content Handling")
print("=" * 90)

with open('extracted_sentences_clean.txt', 'r', encoding='utf-8') as f:
    sentences_content = f.read()

with open('extracted_paragraphs_clean.txt', 'r', encoding='utf-8') as f:
    paragraphs_content = f.read()

# 1. Mathematical notation
print("\n1️⃣  MATHEMATICAL NOTATION:")
print("-" * 90)

# Find the scaled dot product attention formula
scaled_dp = re.search(
    r'Scaled Dot-Product.*?\n(.*?Attention\([^)]+\)[^\.]*\.)',
    paragraphs_content,
    re.DOTALL
)
if scaled_dp:
    text = scaled_dp.group(1)[:400]
    print("\n📐 Scaled Dot-Product Attention Formula:")
    print(f"   {text}")

# 2. Greek letters and subscripts
print("\n\n2️⃣  GREEK LETTERS & SUBSCRIPTS:")
print("-" * 90)

# Find optimizer parameters
optimizer = re.search(r'Adam optimizer.*?β.*?ϵ.*?\.', sentences_content, re.DOTALL)
if optimizer:
    print("\n🔢 Optimizer Parameters:")
    print(f"   {optimizer.group(0)}")

# 3. Figure captions
print("\n\n3️⃣  FIGURE CAPTIONS:")
print("-" * 90)

figures = re.findall(r'Figure \d+[^\.]*\.', sentences_content)
for i, fig in enumerate(figures[:3], 1):
    print(f"\n   Figure {i}: {fig}")

# 4. Table references
print("\n\n4️⃣  TABLE REFERENCES:")
print("-" * 90)

tables = re.findall(r'Table \d+[^\.]*\.', sentences_content)
for i, tab in enumerate(tables[:3], 1):
    print(f"\n   Table {i}: {tab}")

# 5. Complex formula with dimensions
print("\n\n5️⃣  COMPLEX CONTENT WITH DIMENSIONS:")
print("-" * 90)

# Find dimension references
dims = re.findall(r'd[a-z]+ = \d+', paragraphs_content)
if dims:
    print("\n📊 Dimension Specifications:")
    unique_dims = list(set(dims))
    for dim in sorted(unique_dims):
        print(f"   {dim}")

# 6. Citations in context
print("\n\n6️⃣  CITATIONS IN CONTEXT:")
print("-" * 90)

# Find citations with surrounding text
citations_context = re.findall(r'[^\.]*\[\d+(?:,\s*\d+)*\][^\.]*\.', sentences_content)
if citations_context:
    print("\n📚 Examples of citations in sentences:")
    for i, cite in enumerate(citations_context[:3], 1):
        print(f"\n   {i}. {cite[:120]}...")

# 7. Equation references
print("\n\n7️⃣  EQUATIONS & FORMULAS:")
print("-" * 90)

# Find mathematical expressions
equations = re.findall(r'[A-Z]\([A-Za-z,\s]+\)\s*=\s*[^\.]+', paragraphs_content)
if equations:
    print("\n⚗️  Mathematical Expressions:")
    for i, eq in enumerate(equations[:3], 1):
        print(f"\n   {i}. {eq[:150]}...")
else:
    print("\n⚗️  Formula text is preserved as shown in PDF")
    # Show actual example
    formula_example = re.search(
        r'Attention\([^)]+\).*?=.*?softmax.*?\.', 
        paragraphs_content, 
        re.DOTALL
    )
    if formula_example:
        print(f"\n   {formula_example.group(0)[:200]}...")

# 8. Unicode special characters
print("\n\n8️⃣  SPECIAL UNICODE CHARACTERS:")
print("-" * 90)

special_chars = {
    'Asterisk/footnote': '∗',
    'Dagger': '†',
    'Double dagger': '‡',
    'Greek pi': 'π',
    'Greek epsilon': 'ϵ',
    'Multiplication dot': '·',
    'Bullet': '•',
}

print("\n🔤 Unicode characters preserved in extraction:")
for name, char in special_chars.items():
    count = sentences_content.count(char)
    if count > 0:
        print(f"   {name} ({char}): found {count} times")

print("\n" + "=" * 90)

