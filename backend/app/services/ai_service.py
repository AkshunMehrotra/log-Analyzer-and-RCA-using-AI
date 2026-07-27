import os
import certifi
import httpx
import warnings
from dotenv import load_dotenv
from groq import Groq
from app.utils.logger import logger

warnings.filterwarnings("ignore")

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise Exception("GROQ_API_KEY not found in .env")


# SSL Certificate Configuration
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


# Temporary SSL Fix for Groq Connection Issue
http_client = httpx.Client(
    verify=False,
    timeout=60.0
)


client = Groq(
    api_key=api_key,
    http_client=http_client
)



def generate_summary(parsed_result, rca):

    errors = parsed_result.get("errors_count", 0)

    if errors == 0:
        status = "Healthy"

    elif errors <= 3:
        status = "Minor Issues"

    elif errors <= 6:
        status = "Needs Investigation"

    else:
        status = "Critical"



    # Keep AI input limited for large datasets
    MAX_INCIDENTS = 15


    if isinstance(rca, list):

        ai_rca = rca[:MAX_INCIDENTS]

    else:

        ai_rca = str(rca)[:5000]



    logger.info(
        f"Sending {len(ai_rca) if isinstance(ai_rca,list) else 'text'} RCA data to AI"
    )



    prompt = f"""

You are a Senior Contact Center Production Support Engineer.

Generate an enterprise-level Root Cause Analysis report.

The report will be displayed on an AI Log Analyzer dashboard.

Make the report visually attractive using:

- Markdown tables
- Bullet points
- Percentages
- Clear headings
- Relevant emojis



==============================
SYSTEM ANALYSIS DATA
==============================


Total Logs Analyzed:

{parsed_result.get('total_logs')}


Total Errors:

{parsed_result.get('errors_count')}


Total Warnings:

{parsed_result.get('warnings_count')}


Severity:

{parsed_result.get('severity')}



Detected Important Incidents:

{ai_rca}



==============================
RCA REPORT FORMAT
==============================



# Executive Health Dashboard


Create a table:


| Metric | Value |
|---|---|
| Total Logs Processed | |
| Total Errors | |
| Total Warnings | |
| Error Percentage | |
| Warning Percentage | |
| Severity Level | |
| Overall Health Score | |



Calculate:

Error Percentage:

(errors / total logs) * 100


Warning Percentage:

(warnings / total logs) * 100


Health Score:

Give a score between 0-100%.

90-100 : Healthy

70-90 : Warning

Below 70 : Critical



--------------------------------



#  Incident Summary


Explain:

- What happened?
- Which component/service is affected?
- Failure pattern observed from logs.



--------------------------------



#  Root Cause Analysis


Create table:


| Incident | Probable Root Cause | Evidence |
|---|---|---|
| | | |



Explain technical reason behind failures.



--------------------------------



#  Business Impact Analysis


Create table:


| Area | Impact |
|---|---|
| Customer Calls | |
| Agent Productivity | |
| Contact Center Operations | |
| Service Availability | |



--------------------------------



#  Recommended Actions



## Immediate Actions

Provide steps support engineers should perform immediately.



## Preventive Actions

Provide:

- Monitoring improvements
- Alerting improvements
- Automation suggestions
- Infrastructure improvements



--------------------------------



# Final System Assessment


Create table:


| Category | Status |
|---|---|
| System Health | |
| Severity | |
| Investigation Priority | |
| Recommendation | |



Rules:

- Do not give generic answers.
- Use only provided incident information.
- Think like a real production support engineer.
- Keep response concise but detailed.
- Always use markdown tables.

"""



    try:

        logger.info("Calling Groq API for RCA summary")


        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[

                {
                    "role": "system",
                    "content":
                    """
You are an expert Contact Center RCA Engineer.

You specialize in:
- SIP failures
- Network issues
- Database failures
- Application errors
- Production incidents
"""
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],


            temperature=0.1,

            max_tokens=1200

        )



        ai_summary = response.choices[0].message.content.strip()


        logger.info("AI RCA Report generated successfully")



    except Exception as e:


        logger.exception("Groq API Failed")


        ai_summary = f"""

# AI Report Generation Failed


Reason:

{str(e)}


## System Status

{status}


## Logs Processed

{parsed_result.get('total_logs')}


## Errors

{parsed_result.get('errors_count')}


## Warnings

{parsed_result.get('warnings_count')}

"""



    return {


        "analysis_summary": ai_summary,


        "summary": {

            "total_logs": parsed_result.get("total_logs"),

            "errors": parsed_result.get("errors_count"),

            "warnings": parsed_result.get("warnings_count"),

            "severity": parsed_result.get("severity")

        },


        "root_cause_analysis": ai_rca,


        "overall_status": status

    }