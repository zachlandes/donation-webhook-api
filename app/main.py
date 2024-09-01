from fastapi import FastAPI, HTTPException, Header, Depends, Request
from sqlalchemy.orm import Session
from . import models, database, utils
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables on startup
@app.on_event("startup")
async def startup_event():
    models.Base.metadata.create_all(bind=database.engine)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/webhook")
async def receive_webhook(
    request: Request,
    donation: models.DonationCreate,
    x_webhook_token: str = Header(...),
    db: Session = Depends(get_db)
):
    cf_ray = request.headers.get("CF-Ray", "Not available")
    logger.info(f"Received webhook request. CF-Ray: {cf_ray}")

    if x_webhook_token != utils.SECRET_TOKEN:
        logger.warning(f"Unauthorized webhook attempt. CF-Ray: {cf_ray}")
        raise HTTPException(status_code=403, detail="Forbidden")
    
    try:
        # Add donation to database
        db_donation = models.Donation(**donation.dict())
        db.add(db_donation)
        db.commit()
        db.refresh(db_donation)
        logger.info(f"Donation received and stored: {donation.chargeId}. CF-Ray: {cf_ray}")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error processing donation: {str(e)}. CF-Ray: {cf_ray}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/donations")
async def get_donations(token: str, db: Session = Depends(get_db)):
    if token != utils.SECRET_TOKEN:
        logger.warning("Unauthorized API access attempt")
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        donations = db.query(models.Donation).all()
        return donations
    except Exception as e:
        logger.error(f"Error retrieving donations: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    logger.info("Root route accessed")
    return {"message": "Welcome to the Donation Webhook Service"}

@app.head("/")
async def head_root():
    return {}

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Received {request.method} request to {request.url.path}")
    response = await call_next(request)
    logger.info(f"Returned {response.status_code} for {request.method} {request.url.path}")
    return response
