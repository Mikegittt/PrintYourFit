from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.services.cloudinary_service import upload_design_file

router = APIRouter()

@router.post("/design-file")
async def upload_design(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is required")
    file_url = await upload_design_file(file)
    return {"file_url": file_url}
