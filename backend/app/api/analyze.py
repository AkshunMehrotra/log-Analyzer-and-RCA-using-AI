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


router = APIRouter(
    prefix="/api/analyze",
    tags=["Analyze"]
)


@router.get("/analyze")
def analyze(db: Session = Depends(get_db)):

    file_path = get_latest_log()

    if file_path is None:
        return {
            "message": "No file uploaded."
        }


    if file_path.endswith(".csv"):

        result = analyze_csv(file_path)

        analysis = Analysis(
            filename=file_path,
            total_logs=result["total_logs"],
            errors=result["errors_count"],
            warnings=result["warnings_count"],
            severity=result["severity"]
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)


        return {
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

    elif file_path.endswith(".log"):

        result = parse_log(file_path)

        rca = analyze_errors(result["errors"])

        incidents = detect_incident(rca)

        response = generate_summary(result, rca)


        analysis = Analysis(
            filename=file_path,
            total_logs=result["total_logs"],
            errors=result["errors_count"],
            warnings=result["warnings_count"],
            severity=result["severity"]
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)


        return {
            "message": "Log Analysis Completed",

            "statistics":{
                "total_logs": result["total_logs"],
                "errors": result["errors_count"],
                "warnings": result["warnings_count"],
                "severity": result["severity"]
            },
            
            "summary": response["analysis_summary"],

            "incidents": incidents,

            "root_cause_analysis":
                response["root_cause_analysis"],

            "overall_status":
                response["overall_status"]
        }

    else:

        return {
            "message": "Unsupported file format."
        }