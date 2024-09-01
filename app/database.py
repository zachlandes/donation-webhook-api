from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import logging

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable is not set")
    raise ValueError("DATABASE_URL must be set")

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Database connection established")
except Exception as e:
    logger.error(f"Error connecting to database: {str(e)}")
    raise
