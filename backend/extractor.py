import pdfplumber


def extract_text(pdf_file):
    """
    Extracts raw text from a PDF file (page by page).
    pdf_file: a file-like object (e.g. from Flask's request.files)
    Returns: full extracted text as a single string
    """
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text.strip()