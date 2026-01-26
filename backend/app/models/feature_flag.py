from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime
from sqlalchemy.sql import func
from app.db.database import Base
from typing import Optional

class FeatureFlag(Base):
    __tablename__ = "feature_flags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)                
    environment = Column(String, default="prod")    # dev/stage/prod
    description = Column(String)
    enabled = Column(Boolean, default=False)

    # rollout
    rollout_percentage = Column(Integer, default=0)

    # allowlists / targeting
    allowed_users = Column(JSON, default=[])   # list of user ids (whitelist)
    allowed_groups = Column(JSON, default=[])  # list of group names

    # optional metadata scheduling
    start_at = Column(DateTime, nullable=True)  
    end_at = Column(DateTime, nullable=True)    

    extra_metadata = Column(JSON, default={})
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
