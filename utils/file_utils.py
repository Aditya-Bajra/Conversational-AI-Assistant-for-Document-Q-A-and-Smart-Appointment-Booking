import os
import PyPDF2
import docx

def read_txt(file_path: str) -> str:
    """Read content from a text file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf(file_path: str) -> str:
    """Read content from a PDF file."""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text()
        return pdf_text

def read_docx(file_path: str) -> str:
    """Read content from a DOCX file."""
    doc = docx.Document(file_path)
    doc_text = ""
    for para in doc.paragraphs:
        doc_text += para.text
    return doc_text

def load_document(file_path: str) -> str:
    """
    Load the content of a document based on its extension.
    """
    file_extension = file_path.split(".")[-1].lower()

    if file_extension == "txt":
        return read_txt(file_path)
    elif file_extension == "pdf":
        return read_pdf(file_path)
    elif file_extension == "docx":
        return read_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")


# def test_load_document():
#     test_files = [
#         "test_data/sample_doc.txt",
#         "test_data/sample_doc.pdf",
#         "test_data/sample_doc.docx",
#     ]

#     for file_path in test_files:
#         try:
#             print(f"\nReading from: {file_path}")
#             content = load_document(file_path)
#             print("File read successfully. First 200 characters:")
#             print(content[:200] + ("..." if len(content) > 200 else ""))
#         except Exception as e:
#             print(f"Error reading {file_path}: {e}")

# test_load_document()