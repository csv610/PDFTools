import re

# Read the output file
with open('extracted_sentences.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Split by sentence markers
sentences = re.split(r'\n=+\n\n', content.strip())

multi_page_count = 0
single_page_count = 0
sentence_data = []

for sentence_block in sentences:
    lines = sentence_block.split('\n', 1)
    if len(lines) < 2:
        continue
    
    header = lines[0]
    text = lines[1] if len(lines) > 1 else ""
    
    # Extract page info
    match = re.search(r'\[Sentence \d+ - Pages? (.+)\]', header)
    if match:
        page_info = match.group(1)
        is_multi_page = '-' in page_info
        
        if is_multi_page:
            multi_page_count += 1
            sentence_data.append({
                'header': header,
                'pages': page_info,
                'text': text.strip(),
                'has_period': text.strip().endswith(('.', '!', '?'))
            })
        else:
            single_page_count += 1

print(f"Total sentences analyzed: {single_page_count + multi_page_count}")
print(f"Single-page sentences: {single_page_count}")
print(f"Multi-page sentences: {multi_page_count}")
print()

if multi_page_count > 0:
    print("=" * 80)
    print("MULTI-PAGE SENTENCES ANALYSIS:")
    print("=" * 80)
    for i, data in enumerate(sentence_data[:5], 1):
        print(f"\n{data['header']}")
        print(f"Text preview: {data['text'][:100]}...")
        print(f"Ends with punctuation: {data['has_period']}")
        print(f"Length: {len(data['text'])} chars")
