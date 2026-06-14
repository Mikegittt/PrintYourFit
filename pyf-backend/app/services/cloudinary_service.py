import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
from app.core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
)

async def upload_design_file(file: UploadFile) -> str:
    contents = await file.read()
    result = cloudinary.uploader.upload(
        contents,
        resource_type="auto",
        folder="pyf/designs",
    )
    return result.get("secure_url")
