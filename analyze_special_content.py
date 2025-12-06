import re

print("=" * 90)
print("ANALYSIS: How Extraction Handles Special Content")
print("=" * 90)

# Check clean output
with open('extracted_sentences_clean.txt', 'r', encoding='utf-8') as f:
    sentences_content = f.read()

with open('extracted_paragraphs_clean.txt', 'r', encoding='utf-8') as f:
    paragraphs_content = f.read()

print("\n🔬 SPECIAL CONTENT DETECTION:\n")

# 1. LaTeX/Math symbols
latex_patterns = {
    "Subscripts (x_i, h_t)": r'[a-z]_[a-z0-9]',
    "Superscripts (x^2, β²)": r'[a-z]\^[0-9a-z]|[a-z]²',
    "Greek letters (α, β, γ, etc)": r'[α-ω]|β|α|γ|δ|ε|μ|ν|π|σ|τ|φ|ψ|ω',
    "Math operators (√, ∞, ≈)": r'√|∞|≈|±|≤|≥',
    "Fractions/Divisions": r'\d+/\d+|⁄',
    "Exponentials (e^x, 10^-9)": r'e\^|10\^|10−'
}

for label, pattern in latex_patterns.items():
    sentences_matches = len(re.findall(pattern, sentences_content))
    paragraphs_matches = len(re.findall(pattern, paragraphs_content))
    if sentences_matches > 0 or paragraphs_matches > 0:
        print(f"  {label:<40} → Sentences: {sentences_matches:3d}, Paragraphs: {paragraphs_matches:3d}")

# 2. Math notation and formulas
print("\n📐 MATHEMATICAL CONTENT:")
formulas = re.findall(r'[A-Z]\([A-Z,\s]+\)\s*=', sentences_content)
print(f"  Formula patterns found: {len(formulas)}")
if formulas:
    print(f"  Examples: {formulas[:3]}")

# 3. Figure/Table references
print("\n🖼️  FIGURES & TABLES:")
figures = len(re.findall(r'Figure \d+', sentences_content))
tables = len(re.findall(r'Table \d+', sentences_content))
equations = len(re.findall(r'Equation|equation \(\d+\)', sentences_content))
print(f"  Figure references: {figures}")
print(f"  Table references: {tables}")
print(f"  Equation references: {equations}")

# 4. Citations
print("\n📚 CITATIONS & REFERENCES:")
citations = len(re.findall(r'\[\d+(?:,\s*\d+)*\]', sentences_content))
print(f"  Citation brackets found: {citations}")
if citations > 0:
    example_cites = re.findall(r'\[\d+(?:,\s*\d+)*\]', sentences_content)[:5]
    print(f"  Examples: {', '.join(example_cites)}")

# 5. Special Unicode characters
print("\n🔤 SPECIAL CHARACTERS:")
special_chars = re.findall(r'[^\x00-\x7F]+', sentences_content)
unique_special = set(special_chars)
print(f"  Unicode characters found: {len(unique_special)}")
if unique_special:
    print(f"  Examples: {', '.join(list(unique_special)[:10])}")

# 6. Line breaks and structure
print("\n📄 CONTENT STRUCTURE:")
sentences_with_newlines = len(re.findall(r'\n', sentences_content))
paragraphs_with_newlines = len(re.findall(r'\n', paragraphs_content))
print(f"  Sentences with multi-line content: {len(re.findall(r'\]\n[^\[]*\n', sentences_content))}")
print(f"  Paragraphs with multi-line content: {len(re.findall(r'\]\n[^\[]*\n', paragraphs_content))}")

# 7. Actual content examples
print("\n" + "=" * 90)
print("ACTUAL EXAMPLES FROM EXTRACTION:")
print("=" * 90)

# Find sentences with math notation
math_sentences = re.findall(r'\[Sentence \d+ - Page[^\]]*\]\n([^\n]*[a-z]_[a-z0-9][^\n]*(?:\n[^\[=])*)', sentences_content)
if math_sentences:
    print("\n📝 SENTENCE WITH SUBSCRIPTS:")
    print(f"   {math_sentences[0][:200]}...")

# Find paragraph with formulas
formula_paragraphs = re.findall(r'\[Paragraph \d+ - Page[^\]]*\]\n([^\[]*Attention\([^\n]*)', paragraphs_content)
if formula_paragraphs:
    print("\n📐 PARAGRAPH WITH FORMULA:")
    print(f"   {formula_paragraphs[0][:250]}...")

# Find figure references
figure_refs = re.findall(r'.*Figure \d+[^\n]*', sentences_content)
if figure_refs:
    print("\n🖼️  FIGURE REFERENCE:")
    print(f"   {figure_refs[0][:150]}...")

