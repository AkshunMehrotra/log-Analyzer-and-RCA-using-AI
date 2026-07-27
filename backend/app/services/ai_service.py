import os
from dotenv import load_dotenv
from groq import Groq
from app.utils.logger import logger

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise Exception("GROQ_API_KEY not found in .env")

client = Groq(api_key=api_key)


def generate_summary(parsed_result, rca):

    # ---------------- Status ---------------- #

    if parsed_result["errors_count"] == 0:
        status = "Healthy"

    elif parsed_result["errors_count"] <= 3:
        status = "Minor Issues"

    elif parsed_result["errors_count"] <= 6:
        status = "Needs Investigation"

    else:
        status = "Critical"

    # ---------------- Limit RCA ---------------- #

    MAX_RCA = 30

    if len(rca) > MAX_RCA:
        logger.info(
            f"Large RCA Detected ({len(rca)}). Sending only first {MAX_RCA} to AI."
        )
        ai_rca = rca[:MAX_RCA]
    else:
        ai_rca = rca

    prompt = f"""
You are a Senior Contact Center Support Engineer.

Generate a concise RCA Report.

Statistics

Total Logs : {parsed_result['total_logs']}
Errors : {parsed_result['errors_count']}
Warnings : {parsed_result['warnings_count']}
Severity : {parsed_result['severity']}

Analyze ONLY these incidents:

{ai_rca}

Provide:

1. Executive Summary
2. Root Cause
3. Business Impact
4. Recommendations
5. Overall Health

Keep answer under 500 words.
"""

    try:

        logger.info("Calling Groq API")

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
            max_tokens=500
        )

        ai_summary = response.choices[0].message.content.strip()

        logger.info("Groq Response Received Successfully")

    except Exception as e:

        logger.exception("Groq API Failed")

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

    return {

        "analysis_summary": ai_summary,

        "summary": {
            "total_logs": parsed_result["total_logs"],
            "errors": parsed_result["errors_count"],
            "warnings": parsed_result["warnings_count"],
            "severity": parsed_result["severity"]
        },

        "root_cause_analysis": ai_rca,

        "overall_status": status

    }