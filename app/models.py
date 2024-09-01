from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import datetime

Base = declarative_base()

class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    chargeId = Column(String, unique=True, index=True)
    partnerDonationId = Column(String, nullable=True, index=True)
    firstName = Column(String, nullable=True)
    lastName = Column(String, nullable=True)
    email = Column(String, nullable=True)
    toNonprofit = Column(JSON)  # Changed to JSON type
    amount = Column(Float)
    netAmount = Column(Float)
    currency = Column(String)
    frequency = Column(String)
    donationDate = Column(DateTime, default=datetime.utcnow)
    publicTestimony = Column(String, nullable=True)
    privateNote = Column(String, nullable=True)

class DonationCreate(BaseModel):
    chargeId: str
    partnerDonationId: str | None
    firstName: str | None
    lastName: str | None
    email: str | None
    toNonprofit: dict
    amount: float
    netAmount: float
    currency: str
    frequency: str
    donationDate: datetime
    publicTestimony: str | None
    privateNote: str | None

    class Config:
        from_attributes = True
