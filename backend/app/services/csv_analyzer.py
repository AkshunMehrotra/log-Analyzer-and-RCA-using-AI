import pandas as pd


def analyze_csv(file_path):

    df = pd.read_csv(file_path)

    # Remove leading/trailing spaces
    df.columns = df.columns.str.strip()

    print("\nDetected Columns:")
    print(df.columns.tolist())

    errors = []

    required_columns = [
        "Call_ID",
        "Agent_ID",
        "Agent_Name",
        "Date",
        "Customer_ID",
        "Call_Duration_Min",
        "Wait_Time_Sec",
        "Issue_Type",
        "Call_Status",
        "CSAT_Score"
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:

        return {
            "total_logs": len(df),
            "errors_count": len(missing_columns),
            "warnings_count": 0,
            "severity": "HIGH",
            "errors": [
                {
                    "row": 1,
                    "error": f"Missing Column: {col}",
                    "severity": "HIGH",
                    "recommendation": "Check CSV Header."
                }
                for col in missing_columns
            ]
        }


    for i, row in df[df["Agent_Name"].isna()].iterrows():

        errors.append({
            "timestamp": f"Row {i+2}",
            "error": "Missing Agent Name",
            "root_cause": "Agent name is empty.",
            "possible_reasons": [
                "Incomplete data entry"
            ],
            "recommendations": [
                "Fill Agent Name"
            ],
            "severity": "MEDIUM"
        })


    for i, row in df[df["Wait_Time_Sec"].isna()].iterrows():

        errors.append({
            "timestamp": f"Row {i+2}",
            "error": "Missing Wait Time",
            "root_cause": "Wait time missing.",
            "possible_reasons": [
                "System failed to capture value"
            ],
            "recommendations": [
                "Update Wait_Time_Sec"
            ],
            "severity": "LOW"
        })

    for i, row in df[df["CSAT_Score"].isna()].iterrows():

        errors.append({
            "timestamp": f"Row {i+2}",
            "error": "Missing CSAT Score",
            "root_cause": "Customer feedback missing.",
            "possible_reasons": [
                "Customer skipped survey"
            ],
            "recommendations": [
                "Collect CSAT"
            ],
            "severity": "LOW"
        })


    duplicates = df[df.duplicated("Call_ID", keep=False)]

    for i, row in duplicates.iterrows():

        errors.append({
            "timestamp": f"Row {i+2}",
            "error": "Duplicate Call ID",
            "root_cause": "Duplicate Call_ID detected.",
            "possible_reasons": [
                "Duplicate entry"
            ],
            "recommendations": [
                "Remove duplicate Call_ID"
            ],
            "severity": "HIGH"
        })

    for i, row in df[df["Call_Duration_Min"] < 0].iterrows():

        errors.append({
            "timestamp": f"Row {i+2}",
            "error": "Negative Call Duration",
            "root_cause": "Duration cannot be negative.",
            "possible_reasons": [
                "Data entry mistake"
            ],
            "recommendations": [
                "Correct duration"
            ],
            "severity": "HIGH"
        })


    for i, row in df[df["Wait_Time_Sec"] < 0].iterrows():

        errors.append({
            "timestamp": f"Row {i+2}",
            "error": "Negative Wait Time",
            "root_cause": "Wait time cannot be negative.",
            "possible_reasons": [
                "Data entry mistake"
            ],
            "recommendations": [
                "Correct wait time"
            ],
            "severity": "HIGH"
        })


    for i, row in df[df["Call_Duration_Min"] > 300].iterrows():

        errors.append({
            "timestamp": f"Row {i+2}",
            "error": "Outlier Call Duration",
            "root_cause": "Duration unusually high.",
            "possible_reasons": [
                "System issue",
                "Wrong entry"
            ],
            "recommendations": [
                "Verify duration"
            ],
            "severity": "MEDIUM"
        })


    valid_status = ["Resolved", "Escalated", "Closed"]

    for i, row in df.iterrows():

        if row["Call_Status"] not in valid_status:

            errors.append({
                "timestamp": f"Row {i+2}",
                "error": "Invalid Call Status",
                "root_cause": "Unexpected status value.",
                "possible_reasons": [
                    "Invalid data"
                ],
                "recommendations": [
                    "Use Resolved, Escalated or Closed"
                ],
                "severity": "MEDIUM"
            })


    for i, row in df.iterrows():

        try:
            pd.to_datetime(row["Date"], format="%Y-%m-%d")

        except:

            errors.append({
                "timestamp": f"Row {i+2}",
                "error": "Invalid Date",
                "root_cause": "Date format invalid.",
                "possible_reasons": [
                    "Wrong date entered"
                ],
                "recommendations": [
                    "Use YYYY-MM-DD"
                ],
                "severity": "MEDIUM"
            })


    severity = "LOW"

    if len(errors) >= 10:
        severity = "HIGH"

    elif len(errors) >= 5:
        severity = "MEDIUM"


    return {

        "total_logs": len(df),

        "errors_count": len(errors),

        "warnings_count": 0,

        "severity": severity,

        "errors": errors

    }