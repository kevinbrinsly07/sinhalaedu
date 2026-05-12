"""Sinhala language utilities."""

import re


def clean_sinhala_text(text: str) -> str:
    """Clean and normalize Sinhala text."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def validate_sinhala_text(text: str) -> bool:
    """Check if text contains Sinhala characters."""
    # Sinhala Unicode range: U+0D80 to U+0DFF
    sinhala_pattern = r'[\u0D80-\u0DFF]'
    return bool(re.search(sinhala_pattern, text))


def split_sinhala_sentences(text: str) -> list:
    """Split Sinhala text into sentences."""
    # Split by common Sinhala sentence endings
    sentences = re.split(r'[।॥؟]', text)
    return [s.strip() for s in sentences if s.strip()]


def format_sinhala_paper(paper_dict: dict) -> str:
    """Format paper dictionary to printable Sinhala text."""
    output = []
    
    output.append(f"{'='*60}")
    output.append(paper_dict.get('title', 'පරීක්ෂණ පත්‍රය'))
    output.append(f"{'='*60}")
    
    output.append(f"\nමුළු ලකුණු: {paper_dict.get('total_marks')}")
    output.append(f"කාලසීමාව: {paper_dict.get('duration_minutes')} මිනිත්තු")
    
    if paper_dict.get('instructions'):
        output.append(f"\nউපදෙස්:\n{paper_dict['instructions']}")
    
    output.append(f"\n{'='*60}\nප්‍රශ්න\n{'='*60}")
    
    for i, q in enumerate(paper_dict.get('questions', []), 1):
        output.append(f"\n{i}. {q.get('question_text', '')} ({q.get('marks')} ලකුණු)")
        
        if q.get('options'):
            for j, opt in enumerate(q['options'], 1):
                output.append(f"   {chr(96+j)}) {opt}")
    
    return "\n".join(output)
