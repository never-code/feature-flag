from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.schemas.evaluate import EvaluateRequest, EvaluateResponse
from app.services.evaluate_service import evaluate_flag

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/evaluate", response_model=EvaluateResponse)
def evaluate(request: EvaluateRequest, db: Session = Depends(get_db)):
    result,reason = evaluate_flag(
        db=db,
        flag_name=request.flag_name,
        user_id=request.user_id,
        groups=request.groups,
    )
    return EvaluateResponse(enabled=result, reason=reason)


