import pdfplumber
import docx

def extract_text(file_obj, file_type):
    """
    Extracts text from a file object based on the file type.
    
    Args:
        file_obj: The file object (BytesIO) from Streamlit uploader
        file_type: File extension (e.g., 'pdf', 'docx', 'txt')
        
    Returns:
        str: Extracted text
    """
    try:
        if file_type == 'pdf':
            return _extract_from_pdf(file_obj)
        elif file_type == 'docx':
            return _extract_from_docx(file_obj)
        elif file_type == 'txt':
            return str(file_obj.read(), 'utf-8')
        else:
            return ""
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

def _extract_from_pdf(file_obj):
    text = ""
    with pdfplumber.open(file_obj) as pdf:
        for page in pdf.pages:
            # High-fidelity word extraction: looks at physical character gaps
            words = page.extract_words(x_tolerance=3, y_tolerance=3, keep_blank_chars=False)
            
            # Group words by line (y-coordinate) to maintain structure
            lines = {}
            for w in words:
                y = round(w['top'], 1)
                if y not in lines:
                    lines[y] = []
                lines[y].append(w['text'])
            
            # Join words with spaces and lines with newlines
            sorted_y = sorted(lines.keys())
            page_text = "\n".join([" ".join(lines[y]) for y in sorted_y])
            text += page_text + "\n\n"
    return text

def _extract_from_docx(file_obj):
    doc = docx.Document(file_obj)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text
