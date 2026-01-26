from sqlalchemy.orm import Session
from app.models.feature_flag import FeatureFlag
from app.schemas.feature_flag import FeatureFlagCreate, FeatureFlagUpdate
from app.core.redis_client import rdb


def create_flag(db: Session, data: FeatureFlagCreate):
    new_flag = FeatureFlag(**data.model_dump())
    db.add(new_flag)
    db.commit()
    db.refresh(new_flag)
    return new_flag


def get_flag_by_name(db: Session, name: str, environment: str = None):
    return db.query(FeatureFlag).filter(
        FeatureFlag.name == name,
        FeatureFlag.environment == environment
    ).first()


def get_flags(db: Session):
    return db.query(FeatureFlag).all()


def invalidate_cache_for_flag(flag_name: str):
    """
    Delete all cached evaluation results for this feature flag.
    Redis keys look like: eval:<flag_name>:<user_id>:<groups_hash>
    """
    pattern = f"eval:{flag_name}:*"
    keys = rdb.keys(pattern)

    if keys:
        rdb.delete(*keys)


def update_flag(db: Session, name: str, environment: str, data: FeatureFlagUpdate):
    flag = get_flag_by_name(db, name, environment)
    if not flag:
        return None

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(flag, field, value)

    db.commit()
    db.refresh(flag)

    invalidate_cache_for_flag(flag.name)

    return flag



def delete_flag(db: Session, name: str):
    flag = get_flag_by_name(db, name)
    if not flag:
        return None

    invalidate_cache_for_flag(flag.name)

    db.delete(flag)
    db.commit()
    return True
