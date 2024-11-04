from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    JSON,
    LargeBinary,
)  # Use LargeBinary for binary data
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, JSON, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

Base = declarative_base()


class Survey(Base):
    __tablename__ = "surveys"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    questions = Column(JSON)  # Store questions as JSON
    image_data = Column(
        LargeBinary, nullable=True
    )  # Use LargeBinary for storing binary data
    images = relationship("Image", back_populates="survey")  # Link to images


class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"))
    answers = Column(JSON)  # Store answers as JSON


class Image(Base):
    __tablename__ = "images"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    survey_id = Column(Integer, ForeignKey("surveys.id"))
    image_data = Column(LargeBinary, nullable=False)  # Binary image data
    image_name = Column(String)  # Name or label for the image
    survey = relationship("Survey", back_populates="images")  # Link back to survey
