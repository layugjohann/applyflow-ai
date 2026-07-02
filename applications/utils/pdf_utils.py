import fitz  # PyMuPDF


def extract_text_from_pdf(file_or_path):
    """
    Extract text from either:

    - uploaded Django file
    - stored PDF path
    """

    text = ""

    if isinstance(file_or_path, str):

        # Database PDF path
        doc = fitz.open(file_or_path)

    else:

        # Uploaded PDF
        doc = fitz.open(
            stream=file_or_path.read(),
            filetype="pdf"
        )

    for page in doc:
        text += page.get_text()

    return text.strip()