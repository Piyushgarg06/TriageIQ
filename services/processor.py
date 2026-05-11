from fastapi import UploadFile, File
import os 
from fastapi import HTTPException

image_extensions = ['.png']

doc_extensions = [
    '.pdf'                                                      
]
valid_extensions = image_extensions + doc_extensions

def validate_file(file: UploadFile):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in valid_extensions:
        raise HTTPException(
            status_code=400,
            detail="only files with .pdf and .png extension are accepted"
        )
    return {"valid": True}
