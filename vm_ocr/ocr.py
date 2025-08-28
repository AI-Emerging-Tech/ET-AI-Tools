import cv2
from PIL import Image
import numpy as np
import pytesseract
import re
from bs4 import BeautifulSoup 

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

def parse_hocr(hocr_content):
    soup = BeautifulSoup(hocr_content, 'html.parser')
    
    # Extract words with their bounding boxes
    words = []
    for span in soup.find_all('span', class_='ocrx_word'):
        text = span.get_text()
        # Extract bounding box coordinates
        title = span['title']
        bbox = re.search(r'bbox (\d+) (\d+) (\d+) (\d+);', title)
        if bbox:
            x1, y1, x2, y2 = map(int, bbox.groups())
            words.append({
                'text': text,
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2,
                'center_y': (y1 + y2) / 2,
                'center_x': (x1 + x2) / 2
            })
    
    return words

def group_words_into_lines(words, y_tolerance=10):
    # Sort words by their vertical position
    words = sorted(words, key=lambda w: w['center_y'])
    
    lines = []
    current_line = []
    current_y = None
    
    for word in words:
        if current_y is None:
            current_y = word['center_y']
        
        if abs(word['center_y'] - current_y) <= y_tolerance:
            current_line.append(word)
        else:
            # Sort current line words by x position
            current_line = sorted(current_line, key=lambda w: w['x1'])
            lines.append(current_line)
            current_line = [word]
            current_y = word['center_y']
    
    if current_line:
        current_line = sorted(current_line, key=lambda w: w['x1'])
        lines.append(current_line)
    
    return lines

def preprocessImage(image):
    new_size = (image.width * 2, image.height * 2)  # Adjust scaling factor as needed
    image_rescaled = image.resize(new_size, Image.Resampling.LANCZOS)
    np_image_rescaled = np.array(image_rescaled)
    gray_image = cv2.cvtColor(np_image_rescaled, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur
    blurred_image = cv2.GaussianBlur(gray_image, (3, 3), 0)
    binary_image = cv2.adaptiveThreshold(
        blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 37, 1
    )
    return binary_image

def extract_information(hocr_content):
    words = parse_hocr(hocr_content)
    lines = group_words_into_lines(words)
    return lines

def extract_text(image, config, timeout=30):
    """Extract text using basic Tesseract with timeout."""
    try:
        extracted_text = pytesseract.image_to_string(
            image, 
            lang='eng',
            timeout=timeout, 
            config=f'{config} -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$abcdefghijklmnopqrstuvwxyz[]().,@ "'
        )
        return extracted_text
    except Exception as e:
        print(f"Basic text extraction failed: {str(e)}")
        return ""

def extract_and_process_hocr(image, config, timeout=30):
    """Extract text using Tesseract with timeout."""
    try:
        # Set a custom timeout for pytesseract
        extracted_text = pytesseract.image_to_pdf_or_hocr(
            image, 
            lang='eng', 
            extension='hocr',
            timeout=timeout,
            config=f'{config} -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$abcdefghijklmnopqrstuvwxyz[]().,@ " preserve_interword_spaces=1'
        )
        hocr_str = extracted_text.decode('utf-8')
        extracted_text = ""
        
        lines = extract_information(hocr_str)

        for line in lines:
            extracted_text += " ".join(w['text'] for w in line)
            extracted_text += "\n"

        return extracted_text
    
    except Exception as e:
        print(f"OCR extraction failed: {str(e)}")
        # Fallback to simpler extraction method
        return extract_text(image, config, timeout)