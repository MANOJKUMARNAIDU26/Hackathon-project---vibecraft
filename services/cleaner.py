import re

def clean_text(text):
    """
    Cleans the input text by:
    1. Converting to lowercase
    2. Removing special characters and numbers (keeping only alphabets and spaces)
    3. Removing extra whitespace
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and numbers, keep only letters and spaces
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace (multiple spaces/newlines become single space)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
