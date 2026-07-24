import os
import shutil

from fastapi import APIRouter, UploadFile, File

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

UPLOAD_FOLDER = "app/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/")
async def upload(file: UploadFile = File(...)):

    extension = file.filename.split(".")[-1].lower()

    if extension not in ["log", "csv"]:
        return {
            "message": "Only .log and .csv files are supported."
        }

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }