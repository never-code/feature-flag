from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.services.feature_flag_service import create_flag, get_flags
from app.schemas.feature_flag import FeatureFlagCreate, FeatureFlagOut

router = APIRouter(prefix="/flags", tags=["Feature Flags"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=FeatureFlagOut)
def create_feature_flag(flag: FeatureFlagCreate, db: Session = Depends(get_db)):
    return create_flag(db, flag)

@router.get("/", response_model=list[FeatureFlagOut])
def list_feature_flags(db: Session = Depends(get_db)):
    return get_flags(db)
