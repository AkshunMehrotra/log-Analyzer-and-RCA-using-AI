from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from app.api import router
from app.database import Base, engine
from app.models.analysis import Analysis
from app.utils.logger import logger

app = FastAPI(
    title="AI Log Analyzer & RCA Tool",
    description="AI Powered Contact Center Log Analyzer",
    version="1.0.0"
)

# Create Database Tables
Base.metadata.create_all(bind=engine)

logger.info("========================================")
logger.info("AI Log Analyzer Backend Started")
logger.info("Database Connected Successfully")
logger.info("========================================")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


# ---------------- Request Logging ---------------- #

@app.middleware("http")
async def log_requests(request: Request, call_next):

    start = time.time()

    logger.info(
        f"Incoming Request -> {request.method} {request.url.path}"
    )

    try:

        response = await call_next(request)

        duration = round(time.time() - start, 2)

        logger.info(
            f"Completed -> {request.method} {request.url.path} | "
            f"Status={response.status_code} | "
            f"Time={duration}s"
        )

        return response

    except Exception as e:

        logger.exception("Unhandled Exception")

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Something went wrong.",
                "error": str(e)
            }
        )


@app.get("/")
def root():

    logger.info("Health Check Root Endpoint")

    return {
        "success": True,
        "message": "AI Log Analyzer Backend Running"
    }


@app.get("/health")
def health():

    logger.info("Health Endpoint Accessed")

    return {
        "success": True,
        "status": "healthy"
    }