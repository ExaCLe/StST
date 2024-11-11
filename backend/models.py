from sqlalchemy import Column, Integer, String, ForeignKey, JSON, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

Base = declarative_base()


class Survey(Base):
    __tablename__ = "surveys"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    questions = Column(JSON)  # Contains questions with internal_id
    image_data = Column(LargeBinary, nullable=True)
    images = relationship("Image", back_populates="survey")
    responses = relationship("Response", back_populates="survey")


class Response(Base):
    __tablename__ = "responses"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    survey_id = Column(String, ForeignKey("surveys.id"))
    answers = Column(JSON)  # Store answers as JSON
    survey = relationship("Survey", back_populates="responses")


class Image(Base):
    __tablename__ = "images"
    id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: str(uuid.uuid4()))
    survey_id = Column(String, ForeignKey("surveys.id"))
    image_data = Column(LargeBinary, nullable=False)  # Binary image data
    image_name = Column(String)  # Name or label for the image
    survey = relationship("Survey", back_populates="images")  # Link back to survey
