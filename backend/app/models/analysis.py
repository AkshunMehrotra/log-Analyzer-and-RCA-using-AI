from sqlalchemy import Column, Integer, String
from app.database import Base


class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    total_logs = Column(Integer)
    errors = Column(Integer)
    warnings = Column(Integer)
    severity = Column(String)