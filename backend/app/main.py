from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.database import Base, engine

# Import required so SQLAlchemy knows about the table
from app.models.analysis import Analysis

app = FastAPI(
    title="AI Log Analyzer & RCA Tool",
    description="AI Powered Contact Center Log Analyzer",
    version="1.0.0"
)

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "AI Log Analyzer Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }