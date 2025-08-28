from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
from vm_ocr import process_file

app = FastAPI()

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename
    ext = filename.lower().split('.')[-1]
    if ext not in ['pdf', 'docx', 'tif', 'tiff']:
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{ext}') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        result = process_file(filename, tmp_path)
        os.remove(tmp_path)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ASGI server entrypoint
if __name__ == '__main__':
    import asyncio
    from hypercorn.config import Config
    from hypercorn.asyncio import serve

    config = Config()
    config.bind = ["127.0.0.1:12052"]
    asyncio.run(serve(app, config))