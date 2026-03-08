import PyPDF2
import docx
import re

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text(file):
    filename = file.name.lower()
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(file)
    else:
        return ""

# Simple clause highlighting for demo
def highlight_clauses(text):
    clauses = {
        "payment_terms": r"(payment terms|repay.*?installments|interest.*?%)",
        "liability": r"(unlimited liability|liability.*?limited|assumes no additional obligations)",
        "compliance": r"(AML|KYC|regulatory|compliance)",
        "renewal": r"(renewal|auto renewal|termination notice)",
        "penalty": r"(penalty|late fee|late payment)"
    }
    highlights = {}
    for key, pattern in clauses.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        highlights[key] = matches
    return highlights