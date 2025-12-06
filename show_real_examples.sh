#!/bin/bash

echo "════════════════════════════════════════════════════════════════════════════════════"
echo "REAL EXAMPLES FROM paper.pdf EXTRACTION"
echo "════════════════════════════════════════════════════════════════════════════════════"

echo ""
echo "1️⃣  MATHEMATICAL NOTATION & GREEK LETTERS:"
echo "─────────────────────────────────────────────────────────────────────────────────────"
grep -m 1 "β1 = 0.9" extracted_sentences_clean.txt

echo ""
echo "2️⃣  CITATIONS PRESERVED:"
echo "─────────────────────────────────────────────────────────────────────────────────────"
grep -m 1 "long short-term memory" extracted_sentences_clean.txt

echo ""
echo "3️⃣  FIGURE CAPTION:"
echo "─────────────────────────────────────────────────────────────────────────────────────"
grep -m 1 "Figure 1:" extracted_sentences_clean.txt

echo ""
echo "4️⃣  MATHEMATICAL FORMULA (TEXT FORM):"
echo "─────────────────────────────────────────────────────────────────────────────────────"
grep -A 2 "FFN(x)" extracted_sentences_clean.txt | head -5

echo ""
echo "5️⃣  AUTHOR INFORMATION WITH UNICODE SYMBOLS:"
echo "─────────────────────────────────────────────────────────────────────────────────────"
grep -m 1 "Google Brain" extracted_paragraphs_clean.txt | head -3

echo ""
echo "6️⃣  SUBSCRIPT NOTATION:"
echo "─────────────────────────────────────────────────────────────────────────────────────"
grep "d_model\|h_t\|x_" extracted_sentences_clean.txt | head -3

echo ""
echo "7️⃣  SPECIAL CHARACTERS (FOOTNOTE MARKERS):"
echo "─────────────────────────────────────────────────────────────────────────────────────"
grep "∗Equal contribution" extracted_paragraphs_clean.txt

echo ""
echo "════════════════════════════════════════════════════════════════════════════════════"
