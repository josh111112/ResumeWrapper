import pypdf
import docx

def extract_text_from_pdf(file):
    reader = pypdf.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text(uploaded_file):
    try:
        if uploaded_file.name.endswith('.pdf'):
            return extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith('.docx'):
            return extract_text_from_docx(uploaded_file)
        elif uploaded_file.name.endswith('.txt') or uploaded_file.name.endswith('.tex'):
            return uploaded_file.read().decode('utf-8')
        else:
            return None
    except Exception as e:
        return f"Error extracting text: {e}"
