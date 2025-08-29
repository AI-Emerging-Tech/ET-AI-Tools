# vm_ocr

`vm_ocr` is a Python package for extracting text from documents using Optical Character Recognition (OCR). It supports PDF, TIFF, DOCX, and DOC files, leveraging Tesseract OCR, pdf2image, and LibreOffice for robust document processing.

## Features

- Extracts text from PDF, TIFF, DOCX, and DOC files.
- Uses Tesseract OCR with advanced preprocessing for improved accuracy.
- Converts DOCX/DOC to PDF using LibreOffice for OCR compatibility.
- Processes multi-page documents in parallel for efficiency.
- Outputs extracted text per page.

## Requirements

- Python >= 3.7
- Tesseract OCR (must be installed and available in your system path)
- LibreOffice (for DOCX/DOC conversion)
- The following Python packages:
  - pdf2image
  - pytesseract
  - opencv-python
  - numpy
  - beautifulsoup4
  - Pillow
  - langchain-ollama
  - pydantic
  - langchain-core
- For more refer to requirements.txt

## Installation

Install via pip (only for users within the server):

```bash
pip install f"home/{linux_user}/vm_ocr"
```
linux_user = Your "user_name" with in the server. 

Make sure Tesseract OCR and LibreOffice are installed on your system.

## Usage

### Basic OCR Extraction

You can use the main OCR pipeline programmatically:

```python
from vm_ocr import process_file

result = process_file("document.pdf", "/path/to/document.pdf")
for page in result["extracted_text"]:
    print(f"Page {page['page']}:")
    print(page["text"])
```

### Structured Information Extraction

You can extract structured information from raw text using a Pydantic schema and LLM:

```python
from vm_ocr import extract_information_from_text
from vm_ocr.models import CyberInsuranceApplication

raw_text = "...your extracted or input text..."
result = extract_information_from_text(raw_text, schema_model=CyberInsuranceApplication)
print(result)
```

You can also provide a custom prompt or schema for different document types.

## Command-line Usage

You can adapt the commented-out code in `vm_ocr/__init__.py` to process all supported files in a directory and save the output as text files.

## Notes

- For DOCX/DOC files, LibreOffice is used to convert documents to PDF before OCR.
- For best results, ensure Tesseract is correctly installed and accessible at `/usr/bin/tesseract` or update the path in `vm_ocr/ocr.py`.
- The OCR pipeline uses multiprocessing for faster processing of multi-page documents.
- Structured extraction requires a running Ollama server and the appropriate LLM model (e.g., llama3.1:8b).

## License

MIT License

## Author

Dheeraj 
