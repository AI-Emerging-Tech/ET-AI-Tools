import os
from pdf2image import convert_from_path
from PIL import Image
from docx import Document
from PyPDF2 import PdfReader
import tempfile


def pdf_process(file_path):
    try:
        print(f"[PDF PROCESS] Converting PDF: {file_path}")
        images = convert_from_path(file_path)
        print(f"[PDF PROCESS] Converted {len(images)} pages.")
        return images
    except Exception as e:
        print("Error in PDF processing:", e)
        return None

def extract_raw_text_from_pdf(file_path):
    try:
        print(f"[RAW TEXT MODE] Extracting raw text from: {file_path}")
        reader = PdfReader(file_path)
        raw_text_pages = [{"page": i + 1, "text": page.extract_text() or ""} for i, page in enumerate(reader.pages)]
        return raw_text_pages
    except Exception as e:
        print(f"[RAW TEXT MODE ERROR] Failed to extract text: {str(e)}")
        return []

def tif_process(file_path):
    print(f"[TIFF PROCESS] Opening TIFF file: {file_path}")
    return Image.open(file_path)

def extract_raw_text_from_docx(file_path):
    try:
        print(f"[RAW TEXT MODE] Extracting raw text from DOCX: {file_path}")
        doc = Document(file_path)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return [{"page": 1, "text": "\n".join(paragraphs)}]
    except Exception as e:
        print(f"[RAW TEXT MODE ERROR] DOCX text extraction failed: {str(e)}")
        return []
    
def word_process(file_path):
    print(f"[DOCX PROCESS] Converting DOCX to PDF: {file_path}")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Get the base name of the file (without extension) to use for the PDF
        file_name = os.path.basename(file_path)
        pdf_file_name = os.path.splitext(file_name)[0] + ".pdf"
        pdf_path = os.path.join(tmpdir, pdf_file_name)
        
        # Use LibreOffice to convert DOCX to PDF
        cmd = f'libreoffice --headless --convert-to pdf --outdir "{tmpdir}" "{file_path}"'
        cmd_result = os.system(cmd)
        
        # Check the return code of the LibreOffice conversion command
        if cmd_result != 0:
            print(f"[DOCX PROCESS] Error: LibreOffice failed to convert {file_path} to PDF. Return code: {cmd_result}")
            return None
        
        # Debugging: Check the contents of the temporary directory after conversion
        print(f"[DEBUG] Checking contents of temp directory: {tmpdir}")
        print(os.listdir(tmpdir)) 
        
        # Check if the PDF file exists before processing
        if not os.path.exists(pdf_path):
            print(f"[DOCX PROCESS] Error: PDF conversion failed for {file_path}. PDF not found at {pdf_path}")
            return None
        
        # Process the PDF if it exists
        images = pdf_process(pdf_path)
        return images
