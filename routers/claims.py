from fastapi import APIRouter
from services.processor import validate_file
from models.schema import ClaimInput, ClaimOutput
from fastapi import BackgroundTasks
import asyncio
from fastapi import File, UploadFile
import os
router = APIRouter()
from fastapi import HTTPException

@router.post("/claim")
def claim(data: ClaimInput, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_claim, data.claim_id)    
    return ClaimOutput(
        claim_id= data.claim_id,
        status= "received",
        extracted_text= data.description, 
        claim_category= "accident"
        )

@router.post("/claim/upload")
def upload_file(file: UploadFile = File(...)):
    validation = validate_file(file)
    if not validation["valid"]:
        return validation

    file_path = os.path.join("uploads", file.filename)
    with open(file_path, 'wb') as f:
        f.write(file.file.read())
    return {"fileName": file.filename}

async def process_claim(claim_id: str):
    try:
        await asyncio.sleep(3)
        claims[claim_id] = {'status': 'processed'}
        print(f"Processed {claim_id}")
    except Exception as e:
        print(f"Error processing claim {claim_id}: {e}")


claims = {
    '123': {'status': 'processed'},
    '456': {'status': 'under review'}
}

@router.get("/claim/{claim_id}")
def get_claim(claim_id: str):
    if claim_id not in claims:
        raise HTTPException(
            status_code=404,
            detail=f'The claim_id {claim_id} is invalid'
        )
    return claims[claim_id]
    
@router.get("/health")
def health():
    return {
        'status' : 'OK',
        'project' : 'TriageIQ'
    }