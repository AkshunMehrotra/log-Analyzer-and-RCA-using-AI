import os
import shutil
import traceback
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.utils.logger import logger


router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


UPLOAD_FOLDER = "app/uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


ALLOWED_EXTENSIONS = {
    ".log",
    ".csv",
    ".txt"
}


def get_extension(filename):
    return os.path.splitext(filename)[1].lower()


def clear_upload_folder():

    if not os.path.exists(UPLOAD_FOLDER):
        return

    for file in os.listdir(UPLOAD_FOLDER):

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file
        )

        if os.path.isfile(file_path):

            try:

                os.remove(file_path)

                logger.info(
                    f"Deleted previous upload : {file}"
                )

            except Exception as e:

                logger.warning(
                    f"Unable to delete {file} : {e}"
                )


@router.post("/")
async def upload(file: UploadFile = File(...)):

    try:

        logger.info(
            f"Upload Started : {file.filename}"
        )


        # ---------------- Filename Validation ---------------- #

        if not file.filename:

            clear_upload_folder()

            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "message":
                    "Oops! No file was selected."
                }
            )


        # ---------------- Extension Validation ---------------- #

        extension = get_extension(
            file.filename
        )


        if extension not in ALLOWED_EXTENSIONS:

            clear_upload_folder()

            logger.warning(
                f"Unsupported File : {file.filename}"
            )

            raise HTTPException(
                status_code=400,
                detail={

                    "success": False,

                    "message":
                    "Oops! The file you selected is not supported.",

                    "supported_formats":
                    list(ALLOWED_EXTENSIONS)

                }
            )


        # ---------------- Read File ---------------- #

        content = await file.read()


        if len(content) == 0:

            clear_upload_folder()

            raise HTTPException(
                status_code=400,
                detail={

                    "success": False,

                    "message":
                    "The uploaded file is empty."

                }
            )


        # ---------------- Size Validation ---------------- #

        if len(content) > MAX_FILE_SIZE:

            clear_upload_folder()

            raise HTTPException(
                status_code=413,
                detail={

                    "success": False,

                    "message":
                    "File size exceeds maximum allowed limit.",

                    "limit":
                    "10 MB"

                }
            )


        await file.seek(0)


        # ---------------- Remove Previous Upload ---------------- #

        clear_upload_folder()


        # ---------------- Save File ---------------- #

        filename = (
            f"{uuid4().hex}_{file.filename}"
        )


        file_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )


        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


        logger.info(
            f"File Saved Successfully : {filename}"
        )


        return {

            "success": True,

            "message":
            "File uploaded successfully.",

            "filename":
            filename

        }


    except HTTPException:

        raise


    except Exception as e:


        error_trace = traceback.format_exc()


        logger.error(
            f"""
UPLOAD ERROR

Reason:
{str(e)}

Trace:
{error_trace}
"""
        )


        raise HTTPException(

            status_code=500,

            detail={

                "success": False,

                "message":
                "An unexpected error occurred while uploading file.",

                "error_details": {

                    "service":
                    "File Upload Service",

                    "reason":
                    str(e)

                }

            }

        )