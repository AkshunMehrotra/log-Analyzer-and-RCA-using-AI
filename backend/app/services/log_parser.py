import re

from app.utils.logger import logger


def calculate_severity(error_count):

    if error_count >= 3:
        return "CRITICAL"
    elif error_count >= 1:
        return "HIGH"
    else:
        return "LOW"


def parse_log(file_path):

    logger.info(f"Started parsing log file: {file_path}")

    logs = []
    errors = []
    warnings = []

    count = 0

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:

        for line in file:

            count += 1

            match = re.match(r"(.*?) (INFO|WARNING|ERROR) (.*)", line.strip())

            if match:

                log = {
                    "timestamp": match.group(1),
                    "level": match.group(2),
                    "message": match.group(3)
                }

                logs.append(log)

                if log["level"] == "ERROR":
                    errors.append(log)

                elif log["level"] == "WARNING":
                    warnings.append(log)

            if count % 5000 == 0:
                logger.info(f"Processed {count} log records")

    logger.info("Log parsing completed successfully")

    return {

        "total_logs": len(logs),

        "errors_count": len(errors),

        "warnings_count": len(warnings),

        "errors": errors,

        "warnings": warnings,

        "severity": calculate_severity(len(errors))

    }