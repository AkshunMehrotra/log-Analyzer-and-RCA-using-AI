import os

UPLOAD_DIR = "app/uploads"


def get_latest_log():

    files = [
        os.path.join(UPLOAD_DIR, file)
        for file in os.listdir(UPLOAD_DIR)
        if file.endswith((".log", ".csv"))
    ]

    if not files:
        return None

    return max(files, key=os.path.getctime)