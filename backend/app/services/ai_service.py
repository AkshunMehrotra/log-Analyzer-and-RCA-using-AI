import os
from dotenv import load_dotenv
from groq import Groq

# Load .env
load_dotenv()

# Get API Key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise Exception("GROQ_API_KEY not found in .env")

# Initialize Groq Client
client = Groq(api_key=api_key)


def generate_summary(parsed_result, rca):

    # -------------------------
    # Overall Status
    # -------------------------

    if parsed_result["errors_count"] == 0:
        status = "Healthy"

    elif parsed_result["errors_count"] <= 3:
        status = "Minor Issues"

    elif parsed_result["errors_count"] <= 6:
        status = "Needs Investigation"

    else:
        status = "Critical"

    # -------------------------
    # AI Prompt
    # -------------------------

    prompt = f"""
You are a Senior Contact Center Support Engineer.

Analyze the following Contact Center report.

Summary:
{parsed_result}

Detected Issues:
{rca}

Generate a professional report with the following sections:

1. Executive Summary
2. Root Cause Analysis
3. Business Impact
4. Recommendations
5. Overall Health

Write the report in professional English.
Return only the report.
"""

    # -------------------------
    # Generate AI Summary
    # -------------------------

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Contact Center RCA Engineer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=700
        )

        ai_summary = response.choices[0].message.content.strip()

    except Exception as e:

        ai_summary = f"""
Executive Summary

Total Logs : {parsed_result['total_logs']}
Errors : {parsed_result['errors_count']}
Warnings : {parsed_result['warnings_count']}
Severity : {parsed_result['severity']}

Overall Status : {status}

AI Report could not be generated.

Reason:
{str(e)}
"""

    # -------------------------
    # Final Response
    # -------------------------

    return {

        "analysis_summary": ai_summary,

        "summary": {
            "total_logs": parsed_result["total_logs"],
            "errors": parsed_result["errors_count"],
            "warnings": parsed_result["warnings_count"],
            "severity": parsed_result["severity"]
        },

        "root_cause_analysis": rca,

        "overall_status": status

    }