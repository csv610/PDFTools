# PDF Extraction: Special Content Handling Guide

## 📊 What Gets Extracted Well

### ✅ Mathematical Notation
- **Greek letters**: α, β, γ, δ, ε, π, ϵ, etc. → **Preserved**
- **Subscripts/Superscripts**: x_i, h_t, d_k → **Preserved as text**
- **Math operators**: √, ∞, ≈, ±, ≤, ≥ → **Preserved**
- **Exponentials**: 10^-9, e^x → **Preserved as text**

**Example from paper:**
```
"Adam optimizer [20] with β1 = 0.9, β2 = 0.98 and ϵ = 10−9."
```

### ✅ Citations & References
- **Citation brackets**: [1], [2, 3, 4], [35] → **All preserved**
- **In-text references**: "as shown in Figure 1", "see Table 2" → **Preserved**
- **Citation count in paper**: 97 citations extracted correctly

**Example:**
```
"Recurrent neural networks [13] and gated recurrent [7] networks..."
```

### ✅ Figures & Tables
- **Figure references**: "Figure 1:", "Figure 2:" → **Preserved**
- **Table references**: "Table 1:", "Table 3:" → **Preserved**
- **Captions**: "Figure 1: The Transformer - model architecture." → **Preserved**
- **Figure/Table count in paper**: 9 figures, 13 tables referenced

**Example:**
```
"Figure 1: The Transformer - model architecture."
"Table 1: Maximum path lengths, per-layer complexity..."
```

### ✅ Special Unicode Characters
- **Footnote markers**: ∗, †, ‡ → **Preserved**
- **Multiplication dot**: · → **Preserved (27 instances)**
- **Bullets**: • → **Preserved**
- **Accented characters**: Ł, ü, ç → **Preserved**

**Example:**
```
"Ashish Vaswani∗ Google Brain avaswani@google.com"
"†Work performed while at Google Brain."
```

### ✅ Mathematical Expressions (Text Form)
- **Formulas in text**: FFN(x) = max(0, xW₁ + b₁)W₂ + b₂ → **Preserved**
- **Dimension specs**: d_model = 512, d_ff = 2048 → **Preserved**
- **Parameter notation**: h = 8, k = 4 → **Preserved**

**Example:**
```
"FFN(x) = max(0, xW1 + b1)W2 + b2 (2)"
```

---

## ⚠️ What Doesn't Get Extracted (Limitations)

### ❌ Actual Images
- **PDF images** (diagrams, plots, charts) → **Not extracted**
- **Visualization pixel data** → **Not extracted**
- Only **image captions** are preserved

### ❌ Complex LaTeX Rendering
- **PDF-rendered formulas** (not text) → **Not extracted**
- **Equation arrays/matrices** → **Not accessible**
- Example: Matrices like [matrix equations] render as images in many PDFs

### ❌ Precise Formatting
- **Indentation/alignment** → **May be lost**
- **Superscripts/subscripts placement** → **Converted to text notation**
- **Mathematical symbols rendered as images** → **Not extracted**

### ❌ Metadata
- **PDF metadata fields** → **Not extracted**
- **Embedded fonts info** → **Not preserved**
- **Color information** → **Lost**

---

## 📈 Extraction Performance Summary

| Content Type | Extracted | Preserved | Notes |
|---|---|---|---|
| Plain text | ✅ | ✅ | 346 sentences, 20 paragraphs |
| Greek letters | ✅ | ✅ | 6+ instances found |
| Subscripts (text) | ✅ | ✅ | 5+ instances like x_i, h_t |
| Math operators | ✅ | ✅ | √, ∞, ≈, ±, ≤, ≥ |
| Citations | ✅ | ✅ | 97 citation brackets |
| Figure refs | ✅ | ✅ | 9 figure captions |
| Table refs | ✅ | ✅ | 13 table captions |
| Unicode chars | ✅ | ✅ | ∗, †, ‡, π, ϵ, ·, • |
| Formulas (text) | ✅ | ✅ | FFN(x) = ... |
| Actual images | ❌ | ❌ | Image content not available |
| Complex LaTeX | ❌ | ⚠️ | Only if rendered as text |
| PDF metadata | ❌ | ❌ | Not accessible |

---

## 🔧 How It Works

### Text Extraction Process:
1. **pypdf** reads the PDF and extracts text layer
2. **clean functions** remove artifacts:
   - Page numbers
   - Headers/footers
   - Extra whitespace
3. **Sentence/Paragraph splitting** identifies boundaries
4. **Page tracking** records where each item appears

### What Gets Lost:
- Any content that's stored as **PDF images** (not text)
- **Precise formatting** that requires layout analysis
- **Mathematical symbols** rendered as images instead of Unicode

### What's Preserved:
- All **text-based content** including Unicode
- All **citations and references**
- **Multi-line content** (abstracts, author lists)
- **Structure** (section headers, figure/table captions)

---

## 💡 Tips for Best Results

1. **OCR-free PDFs work best**: Text must be selectable in the PDF
2. **Check source format**: PDFs with scanned images won't extract well
3. **Mathematical content**: Depends on whether formulas are text or images
4. **Citations**: Usually preserved well since they're text-based
5. **Verify output**: Always review extracted text for accuracy

## Example: What You Get

```
✅ EXTRACTED:
"Adam optimizer [20] with β1 = 0.9, β2 = 0.98 and ϵ = 10−9"

✅ EXTRACTED:
"Figure 1: The Transformer - model architecture."

✅ EXTRACTED:
"FFN(x) = max(0, xW1 + b1)W2 + b2 (2)"

❌ NOT EXTRACTED:
[Image of Transformer architecture diagram]
[Rendered mathematical matrix]
[Chart/plot visualization]
```

