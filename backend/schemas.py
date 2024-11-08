# schemas.py
from pydantic import BaseModel, Field
from typing import List, Any, Optional


class SurveyCreate(BaseModel):
    name: str
    questions: List[Any]


class ResponseCreate(BaseModel):
    answers: dict


class Question(BaseModel):
    text: str
    type: str
    options: Optional[List[str]] = []
    image: Optional[str] = None  # Base64 image data
    scale_points: Optional[int] = None
    imageName: Optional[str] = None  # Use imageName consistently


class SurveyDirectCreate(BaseModel):
    adminPassword: str
    title: str
    questions: List[Question]
