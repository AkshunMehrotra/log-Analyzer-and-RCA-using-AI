from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.analysis import Analysis

from app.services.file_manager import get_latest_log
from app.services.log_parser import parse_log
from app.services.rca_engine import analyze_errors
from app.services.ai_service import generate_summary
from app.services.incident_detector import detect_incident
from app.services.csv_analyzer import analyze_csv

from app.utils.logger import logger

router = APIRouter(
    prefix="/api/analyze",
    tags=["Analyze"]
)


@router.get("/analyze")
def analyze(db: Session = Depends(get_db)):

    try:

        logger.info("Analysis Started")

        file_path = get_latest_log()

        if file_path is None:
            logger.warning("No uploaded file found.")
            return {
                "success": False,
                "message": "No file uploaded."
            }

        logger.info(f"Latest File : {file_path}")

        # ================= CSV ================= #

        if file_path.endswith(".csv"):

            logger.info("CSV Analysis Started")

            result = analyze_csv(file_path)

            try:
                analysis = Analysis(
                    filename=file_path,
                    total_logs=result["total_logs"],
                    errors=result["errors_count"],
                    warnings=result["warnings_count"],
                    severity=result["severity"]
                )

                db.add(analysis)
                db.commit()

                logger.info("CSV Analysis saved to database")

            except Exception as db_error:

                logger.exception("Database Error")
                db.rollback()

            return {

                "success": True,

                "message": "CSV Analysis Completed",

                "summary": {
                    "total_rows": result["total_logs"],
                    "errors": result["errors_count"],
                    "warnings": result["warnings_count"],
                    "severity": result["severity"]
                },

                "errors_found": result["errors"],

                "overall_status":
                    "Needs Investigation"
                    if result["errors_count"]
                    else "Healthy"
            }

        # ================= LOG ================= #

        elif file_path.endswith(".log"):

            logger.info("Parsing Log File")

            result = parse_log(file_path)

            logger.info("Generating RCA")

            rca = analyze_errors(result["errors"])

            logger.info(f"Total RCA Records : {len(rca)}")

            logger.info("Detecting Incidents")

            incidents = detect_incident(rca)

            logger.info("Preparing AI Summary")

            # AI ko sirf top 50 RCA bhejna
            top_rca = rca[:50]

            response = generate_summary(result, top_rca)

            logger.info("AI Summary Generated")

            try:

                analysis = Analysis(
                    filename=file_path,
                    total_logs=result["total_logs"],
                    errors=result["errors_count"],
                    warnings=result["warnings_count"],
                    severity=result["severity"]
                )

                db.add(analysis)
                db.commit()

                logger.info("Analysis Saved Successfully")

            except Exception:

                logger.exception("Database Error")
                db.rollback()

            return {

                "success": True,

                "message": "Log Analysis Completed",

                "statistics": {

                    "total_logs": result["total_logs"],

                    "errors": result["errors_count"],

                    "warnings": result["warnings_count"],

                    "severity": result["severity"]

                },

                "summary": response["analysis_summary"],

                # Limit response size
                "incidents": incidents[:20],

                "root_cause_analysis": rca[:100],

                "total_incidents": len(incidents),

                "total_rca_records": len(rca),

                "overall_status": response["overall_status"]

            }

        else:

            logger.warning("Unsupported file uploaded")

            return {

                "success": False,

                "message": "Unsupported file format."

            }

    except Exception as e:

        logger.exception("Unexpected Error During Analysis")

        return {

            "success": False,

            "message": "Analysis failed gracefully.",

            "error": str(e)

        }