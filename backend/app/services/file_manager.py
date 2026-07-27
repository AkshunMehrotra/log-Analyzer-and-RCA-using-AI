import os
from app.utils.logger import logger

UPLOAD_DIR = "app/uploads"

ALLOWED_EXTENSIONS = (".log", ".csv")


def get_latest_log():

    if not os.path.exists(UPLOAD_DIR):

        logger.warning("Upload directory not found.")

        return None


    files = [

        os.path.join(UPLOAD_DIR, file)

        for file in os.listdir(UPLOAD_DIR)

        if file.lower().endswith(ALLOWED_EXTENSIONS)

    ]


    if not files:

        logger.warning("No supported uploaded files found.")

        return None


    latest_file = max(files, key=os.path.getctime)

    logger.info(f"Latest uploaded file selected : {latest_file}")

    return latest_file