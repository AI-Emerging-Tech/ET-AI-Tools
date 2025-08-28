from vm_ocr import ocr
from .file_extensions_process import pdf_process, word_process, tif_process, extract_raw_text_from_pdf, extract_raw_text_from_docx
import multiprocessing
import traceback


def batch_process_ocr_text_extraction(batch_data):
    result = []
    idx = batch_data[0]
    print(f"[OCR BATCH] Starting batch {idx} with {len(batch_data[1])} pages.")
    
    for page_num, image in enumerate(batch_data[1], start=1):
        try:
            print(f"[OCR PAGE] Preprocessing image in batch {idx}, page {page_num}")
            final_image = ocr.preprocessImage(image)
            config = '--oem 3 --psm 12'
            extracted_text = ocr.extract_and_process_hocr(final_image, config, timeout=30)

            if not extracted_text.strip():
                print(f"[OCR PAGE] Empty output on page {page_num}, retrying with timeout=60")
                extracted_text = ocr.extract_and_process_hocr(final_image, config, timeout=60)

            print(f"[OCR PAGE] OCR output length (chars): {len(extracted_text)} for page {page_num}")
            result.append(extracted_text)
        except Exception as e:
            print(f"[OCR ERROR] Page {page_num} in batch {idx} failed: {str(e)}")
            result.append("")
    
    print(f"[OCR BATCH] Completed batch {idx} with {len(result)} results")
    return idx, result

def process_file(file_name: str, file_path: str, raw_text_mode: bool = False, docx_raw_text_mode: bool = False):
    try:
        print(f"\n[START] Processing: {file_name}")
        
        if file_name.lower().endswith('.pdf'):
            if raw_text_mode:
                extracted_pages = extract_raw_text_from_pdf(file_path)
                print(f"[COMPLETE] Raw text extracted from {len(extracted_pages)} PDF pages\n")
                return {"extracted_text": extracted_pages}
            else:
                images = pdf_process(file_path)
                page_count = len(images)

        elif file_name.lower().endswith('.docx'):
            if docx_raw_text_mode:
                extracted_pages = extract_raw_text_from_docx(file_path)
                print(f"[COMPLETE] Raw text extracted from DOCX\n")
                return {"extracted_text": extracted_pages}
            else:
                images = word_process(file_path)
                page_count = len(images)

        elif file_name.lower().endswith(('.tif', '.tiff')):
            image = tif_process(file_path)
            images = [image]
            page_count = 1

        else:
            raise Exception('File format not supported')

        print(f"[INFO] Total pages: {page_count}")

        ocr_num_processes = min(page_count, max(1, multiprocessing.cpu_count() // 8))
        batch_size = max(1, page_count // ocr_num_processes)
        print(f"[INFO] Using {ocr_num_processes} processes, batch size: {batch_size}")

        ocr_batches = [(idx, images[i:i+batch_size]) for idx, i in enumerate(range(0, page_count, batch_size))]
        extracted_text_batch = {}
        extracted_text = []
 
        # Use explicit pool management instead of context manager
        pool = None
        try:
            pool = multiprocessing.Pool(ocr_num_processes)
            
            # Use map instead of imap for better reliability
            results = pool.map(batch_process_ocr_text_extraction, ocr_batches)
     
            # Process results
            for result in results:
                extracted_text_batch.update({result[0]: result[1]})
            
        except Exception as pool_error:
            print(f"[ERROR] Multiprocessing pool failed: {pool_error}")
            traceback.print_exc()
            
            # Fallback to sequential processing
            extracted_text_batch = {}
            for batch in ocr_batches:
                try:
                    result = batch_process_ocr_text_extraction(batch)
                    extracted_text_batch.update({result[0]: result[1]})
                except Exception as batch_error:
                    print(f"[ERROR] Batch processing failed: {batch_error}")
                    extracted_text_batch.update({batch[0]: [""]})
        
        finally:
            # Ensure pool is properly closed
            if pool is not None:
                try:
                    pool.close()
                    pool.join()
                except Exception as close_error:
                    print(f"[ERROR] Error closing pool: {close_error}")
                    try:
                        pool.terminate()
                        pool.join()
                    except Exception as term_error:
                        print(f"[ERROR] Error terminating pool: {term_error}")

        # Assemble results in correct order
        for idx in range(len(ocr_batches)):
            batch_result = extracted_text_batch.get(idx, [])
            extracted_text.extend(batch_result)

        print(f"[COMPLETE] Total OCR pages processed: {len(extracted_text)}\n")
        
        extracted_pages = [{"page": i + 1, "text": text} for i, text in enumerate(extracted_text)]

        return_obj = {
            "extracted_text": extracted_pages
        }
        return return_obj

    except Exception as e:
        print(f"[ERROR] Exception in process_file: {str(e)}")
        traceback.print_exc()
        return {"extracted_text": []}


