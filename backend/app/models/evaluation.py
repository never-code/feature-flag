from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..db.database import Base



class FeatureEvaluation(Base):
    __tablename__ = "feature_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    flag_name = Column(String, ForeignKey("feature_flags.name"), nullable=False)
    user_id = Column(String, nullable=True)
    result = Column(Boolean, nullable=False)
    reason = Column(String, nullable=False)

    # Relationship back to main FeatureFlag model
    flag = relationship("FeatureFlag", backref="evaluations")
