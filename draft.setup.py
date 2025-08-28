from setuptools import setup, find_packages

setup(
    name="vm_ocr",
    version="0.0.4",
    description="Document OCR pipeline: extract text from PDF, TIFF, DOCX, and DOC files using Tesseract, pdf2image, and LibreOffice.",
    author="Dheeraj Bhupathiraju",
    author_email="dheerajvarma.bhupathiraju@valuemomentum.com",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
    "pdf2image>=1.16.2",
    "pytesseract>=0.3.9",
    "opencv-python>=4.5.5.64",
    "numpy>=1.22.1",
    "beautifulsoup4>=4.11.0",
    "python-docx>=1.1.0"
    ],
)