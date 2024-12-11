import re


def clean_text(text):
    # Step 1: Strip leading and trailing whitespace
    text = text.strip()
 
    # Step 2: Replace multiple spaces with a single space
    text = ' '.join(text.split())
 
    # Step 3: Replace newline characters with spaces
    text = text.replace('\n', ' ').replace('\r', ' ')
 
    # Step 4: Remove spaces around hyphens
    text = re.sub(r'\s*-\s*', '-', text)
 
    return text.strip()
 






