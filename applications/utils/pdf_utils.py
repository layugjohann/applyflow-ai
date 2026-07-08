import fitz  # PyMuPDF


def extract_text_from_pdf(file_or_path):
    """
    Extract text from either:
    - local PDF path
    - Django FieldFile (Supabase/S3)
    - Uploaded file
    """

    text = ""

    if isinstance(file_or_path, str):
        doc = fitz.open(file_or_path)

    else:
        file_or_path.open("rb")

        try:
            file_or_path.seek(0)   # <-- Add this
            pdf_bytes = file_or_path.read()

            doc = fitz.open(
                stream=pdf_bytes,
                filetype="pdf"
            )

        finally:
            file_or_path.close()

    for page in doc:
        text += page.get_text()

    doc.close()

    return text.strip()