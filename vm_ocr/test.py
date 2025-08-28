from vm_ocr import process_file

if __name__ == "__main__":
    # Example usage: change these paths to your actual file
    file_name = "Business_Continuity_Plan.pdf"
    file_path = "/home/dbhupathiraju/ET-AI-OCR/Business_Continuity_Plan.pdf"

    result = process_file(file_name, file_path)
    print(result)