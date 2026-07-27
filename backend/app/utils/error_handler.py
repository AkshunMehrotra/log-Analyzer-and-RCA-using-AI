import traceback
from app.utils.logger import logger


def handle_error(error, component="System"):

    traceback_details = traceback.extract_tb(
        error.__traceback__
    )

    if traceback_details:

        last_error = traceback_details[-1]

        file_name = last_error.filename.split("\\")[-1]
        line_number = last_error.lineno
        function_name = last_error.name

    else:

        file_name = "Unknown"
        line_number = "Unknown"
        function_name = "Unknown"


    logger.exception(
        f"""
ERROR OCCURRED

Component:
{component}

File:
{file_name}

Line:
{line_number}

Function:
{function_name}

Reason:
{str(error)}
"""
    )


    return {

        "success": False,

        "message":
        "An error occurred while processing your request.",

        "error_details": {

            "component": component,

            "file": file_name,

            "line": line_number,

            "function": function_name,

            "reason": str(error)

        }

    }