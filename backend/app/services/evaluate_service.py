import json, hashlib
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.core.redis_client import rdb
from app.services.feature_flag_service import get_flag_by_name
from app.models.evaluation import FeatureEvaluation

def user_bucket(user_id: str) -> int:
    if not user_id:
        return -1
    hashed = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
    return hashed % 100


def evaluate_flag(db: Session, flag_name: str, user_id: str, groups: list, environment: str = "dev"):

    groups_key = "-".join(sorted(groups)) if groups else "none"
    cache_key = f"eval:{environment}:{flag_name}:{user_id}:{groups_key}"

    # Try reading from redis
    cached = rdb.get(cache_key)
    if cached:
        cached = json.loads(cached)
        return cached["result"], cached["reason"]

    flag = get_flag_by_name(db, flag_name, environment=environment)

    if not flag:
        result, reason = False, "flag-not-found"
    else:

        # Priority 1 — user allowlist
        if flag.allowed_users and user_id in flag.allowed_users:
            result, reason = True, "user-whitelist"

        # Priority 2 — group allowlist
        elif flag.allowed_groups and any(g in flag.allowed_groups for g in groups):
            result, reason = True, "group-whitelist"

        # Priority 3 — scheduling
        else:
            now = datetime.now(timezone.utc)

            if flag.start_at and now < flag.start_at.replace(tzinfo=timezone.utc):
                result, reason = False, "before-start"

            elif flag.end_at and now > flag.end_at.replace(tzinfo=timezone.utc):
                result, reason = False, "after-end"

            else:
                # Priority 4 — % rollout
                if flag.rollout_percentage and flag.rollout_percentage > 0:
                    bucket = user_bucket(user_id)

                    if 0 <= bucket < flag.rollout_percentage:
                        result, reason = True, "percentage-rollout"
                    else:
                        result, reason = False, "rollout"
                else:
                    # fallback → default enabled
                    result, reason = bool(flag.enabled), "default"

    try:
        eval_row = FeatureEvaluation(
            flag_name=flag_name,
            user_id=user_id,
            result=result,
            reason=reason
        )
        db.add(eval_row)
        db.commit()
    except Exception:
        db.rollback()

    rdb.setex(cache_key, 3600, json.dumps({"result": result, "reason": reason}))

    return result, reason
