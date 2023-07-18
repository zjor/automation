from datetime import datetime

from sqlalchemy import Column, select
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, DateTime
from sqlalchemy import String
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()


class JobDefinition(Base):
    __tablename__ = "job_definition"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    action = Column(JSONB, nullable=False)
    schedule = Column(String, nullable=False)
    arguments = Column(JSONB, nullable=False)
    output = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    @staticmethod
    def create(engine, user_id: int, action: dict, schedule: str, arguments: dict, output: dict):
        with Session(engine) as session:
            instance = JobDefinition(
                user_id=user_id,
                action=action,
                schedule=schedule,
                arguments=arguments,
                output=output
            )
            session.add(instance)
            session.commit()
            return instance

    @staticmethod
    def find_all(engine):
        with Session(engine) as session:
            query = select(JobDefinition).order_by(JobDefinition.created_at.desc())
            return session.execute(query).all()
