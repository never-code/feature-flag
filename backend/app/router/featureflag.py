from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.schemas.feature_flag import FeatureFlagCreate, FeatureFlagUpdate, FeatureFlagOut
from app.services.feature_flag_service import (
    create_flag, get_flag_by_name, get_flags, update_flag, delete_flag
)
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/flags/", response_model=FeatureFlagOut)
def create_feature_flag(data: FeatureFlagCreate, db: Session = Depends(get_db)):
    existing = get_flag_by_name(db, data.name)
    if existing:
        raise HTTPException(status_code=400, detail="Feature flag already exists")

    return create_flag(db, data)

@router.get("/flags/", response_model=list[FeatureFlagOut])
def list_feature_flags(db: Session = Depends(get_db)):
    return get_flags(db)


@router.get("/flags/{name}", response_model=FeatureFlagOut)
def get_feature_flag(name: str, environment: str = "prod", db: Session = Depends(get_db)):
    flag = get_flag_by_name(db, name, environment)
    if not flag:
        raise HTTPException(status_code=404, detail="Flag not found")
    return flag


@router.put("/flags/{environment}/{name}", response_model=FeatureFlagOut)
def update_feature_flag(environment: str, name: str, data: FeatureFlagUpdate, db: Session = Depends(get_db)):
    updated = update_flag(db, name, environment, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Flag not found")
    return updated

@router.delete("/flags/{name}")
def delete_feature_flag_route(name: str, db: Session = Depends(get_db)):
    deleted = delete_flag(db, name)
    if not deleted:
        raise HTTPException(status_code=404, detail="Flag not found")
    return {"status": "deleted"}