from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Survey(Base):
    __tablename__ = "surveys"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    questions = Column(JSON)  # Store questions as JSON


class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"))
    answers = Column(JSON)  # Store answers as JSON
