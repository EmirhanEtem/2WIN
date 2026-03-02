from sqlalchemy import Column, String, Float, Integer, JSON, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DBEvent(Base):
    """
    Persistent storage model for all tracked system events.
    Used for historical pattern discovery and behavioral playback.
    """
    __tablename__ = 'events'

    id = Column(String, primary_key=True)
    event_type = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)
    payload = Column(JSON, nullable=False)

class Session(Base):
    """
    Represents a contiguous block of user activity (e.g. \"Work Session\").
    """
    __tablename__ = 'sessions'

    id = Column(String, primary_key=True)
    start_time = Column(DateTime, index=True, nullable=False)
    end_time = Column(DateTime, nullable=True)
    duration_seconds = Column(Float, nullable=True)
    metadata_json = Column(JSON, nullable=True)
