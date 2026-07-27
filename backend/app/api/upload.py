import os
import shutil
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.utils.logger import logger

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

UPLOAD_FOLDER = "app/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/")
async def upload(file: UploadFile = File(...)):

    logger.info(f"Upload Started : {file.filename}")

    if not file.filename:
        logger.error("No filename received")
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    extension = file.filename.split(".")[-1].lower()

    if extension not in ["log", "csv"]:
        logger.warning(f"Unsupported File : {file.filename}")
        raise HTTPException(
            status_code=400,
            detail="Only .log and .csv files are supported."
        )

    content = await file.read()

    if len(content) == 0:
        logger.warning("Empty file uploaded")
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    if len(content) > MAX_FILE_SIZE:
        logger.warning("Large file uploaded")
        raise HTTPException(
            status_code=413,
            detail="Maximum allowed file size is 10 MB."
        )

    await file.seek(0)

    filename = f"{uuid4().hex}_{file.filename}"

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    try:

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"File Saved : {filename}")

        return {
            "success": True,
            "message": "File uploaded successfully.",
            "filename": filename
        }

    except Exception:

        logger.exception("Upload Failed")

        raise HTTPException(
            status_code=500,
            detail="Unable to upload file."
        )