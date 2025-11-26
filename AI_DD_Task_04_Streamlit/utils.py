
import PyPDF2
import io

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts text from an uploaded PDF file.

    Args:
        pdf_file: A file-like object representing the uploaded PDF.

    Returns:
        A string containing all the text extracted from the PDF.
    """
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

