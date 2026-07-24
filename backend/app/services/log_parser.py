import re


def calculate_severity(error_count):

    if error_count >= 3:
        return "CRITICAL"
    elif error_count >= 1:
        return "HIGH"
    else:
        return "LOW"


def parse_log(file_path):

    logs = []

    with open(file_path, "r") as file:

        for line in file.readlines():

            match = re.match(r"(.*?) (INFO|WARNING|ERROR) (.*)", line.strip())

            if match:

                logs.append({
                    "timestamp": match.group(1),
                    "level": match.group(2),
                    "message": match.group(3)
                })

    errors = [log for log in logs if log["level"] == "ERROR"]
    warnings = [log for log in logs if log["level"] == "WARNING"]

    return {
        "total_logs": len(logs),
        "errors_count": len(errors),
        "warnings_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "severity": calculate_severity(len(errors))
    }