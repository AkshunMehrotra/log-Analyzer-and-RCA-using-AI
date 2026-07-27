from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import os
import traceback

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

        logger.info("==============================")
        logger.info("Analysis Started")
        logger.info("==============================")


        # ---------------- Get Latest Uploaded File ---------------- #

        file_path = get_latest_log()


        if not file_path:


            logger.warning(
                "No valid uploaded file found"
            )


            return {

                "success": False,

                "message":
                "No valid file found. Please upload a supported log file first."

            }



        logger.info(
            f"Analyzing File : {file_path}"
        )



        # ---------------- File Exists Check ---------------- #

        if not os.path.exists(file_path):


            logger.error(
                f"File does not exist : {file_path}"
            )


            return {

                "success":False,

                "message":
                "Uploaded file no longer exists. Please upload again."

            }




        extension = os.path.splitext(
            file_path
        )[1].lower()



        # ==========================================================
        #                       CSV ANALYSIS
        # ==========================================================


        if extension == ".csv":


            logger.info(
                "CSV Analysis Started"
            )


            result = analyze_csv(
                file_path
            )



            save_analysis(
                db,
                file_path,
                result
            )



            return {


                "success":True,


                "message":
                "CSV Analysis Completed",



                "statistics":{

                    "total_rows":
                    result.get("total_logs"),


                    "errors":
                    result.get("errors_count"),


                    "warnings":
                    result.get("warnings_count"),


                    "severity":
                    result.get("severity")

                },



                "overall_status":

                    "Critical"
                    if result.get("errors_count",0) > 0

                    else "Healthy"


            }




        # ==========================================================
        #                       LOG ANALYSIS
        # ==========================================================


        elif extension in [".log",".txt"]:



            logger.info(
                "Parsing Log File"
            )



            result = parse_log(
                file_path
            )



            logger.info(
                "Generating RCA"
            )



            rca = analyze_errors(
                result.get("errors",[])
            )



            logger.info(
                f"RCA Records Generated : {len(rca)}"
            )



            logger.info(
                "Detecting Incidents"
            )


            incidents = detect_incident(
                rca
            )



            logger.info(
                "Generating AI Summary"
            )



            # Send limited data to AI
            # Supports 100k+ logs

            top_rca = rca[:20]



            response = generate_summary(
                result,
                top_rca
            )



            logger.info(
                "AI Summary Generated Successfully"
            )



            save_analysis(
                db,
                file_path,
                result
            )



            return {


                "success":True,


                "message":
                "Log Analysis Completed",



                "statistics":{


                    "total_logs":
                    result.get("total_logs"),


                    "errors":
                    result.get("errors_count"),


                    "warnings":
                    result.get("warnings_count"),


                    "severity":
                    result.get("severity")

                },



                "summary":
                response.get("analysis_summary"),



                "incidents":
                incidents[:20],



                "root_cause_analysis":
                rca[:20],



                "total_incidents":
                len(incidents),



                "total_rca_records":
                len(rca),



                "overall_status":
                response.get("overall_status")

            }





        else:


            logger.warning(
                f"Unsupported format : {extension}"
            )



            return {


                "success":False,


                "message":
                "Oops! The uploaded file format is not supported.",



                "supported_formats":[

                    ".log",
                    ".csv",
                    ".txt"

                ]

            }





    except Exception as e:


        error_trace = traceback.format_exc()


        logger.error(
            f"""
ANALYSIS FAILED

Reason:
{str(e)}

Trace:
{error_trace}
"""
        )



        return {


            "success":False,


            "message":
            "Oops! Something went wrong while analyzing the file.",



            "error_details":{


                "service":
                "Analysis Engine",



                "reason":
                str(e)

            }

        }




# ==========================================================
#                  DATABASE SAVE FUNCTION
# ==========================================================


def save_analysis(db, file_path, result):

    try:


        analysis = Analysis(

            filename=file_path,


            total_logs=result.get(
                "total_logs",
                0
            ),


            errors=result.get(
                "errors_count",
                0
            ),


            warnings=result.get(
                "warnings_count",
                0
            ),


            severity=result.get(
                "severity",
                "UNKNOWN"
            )

        )


        db.add(
            analysis
        )


        db.commit()



        logger.info(
            "Analysis Saved Successfully"
        )


    except Exception:


        logger.exception(
            "Database Save Failed"
        )


        db.rollback()