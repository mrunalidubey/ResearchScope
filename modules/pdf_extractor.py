
import pymupdf


def extract_text(pdf_path):

    document = pymupdf.open(pdf_path)

    extracted_text = ""

    for page in document:
        extracted_text += page.get_text() + "\n"

    document.close()

    return extracted_text