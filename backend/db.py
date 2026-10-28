import os
from datetime import datetime, timezone
from sqlalchemy import (create_engine, Column, String, Integer,
                        Float, Boolean, DateTime, ForeignKey)
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def now():
    return datetime.now(timezone.utc)


class Student(Base):
    __tablename__ = "students"
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=now)


class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, ForeignKey("students.id"))
    question_id = Column(String)
    concept_id = Column(String)
    selected = Column(Integer)
    correct = Column(Boolean)
    created_at = Column(DateTime, default=now)


class Mastery(Base):
    __tablename__ = "mastery"
    student_id = Column(String, ForeignKey("students.id"), primary_key=True)
    concept_id = Column(String, primary_key=True)
    value = Column(Float, default=0.5)


def init_db():
    Base.metadata.create_all(engine)