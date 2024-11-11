# schemas.py
from pydantic import BaseModel, Field
from typing import List, Any, Optional


class SurveyCreate(BaseModel):
    name: str
    questions: List[Any]


class ResponseCreate(BaseModel):
    answers: dict


class Condition(BaseModel):
    questionId: Optional[int]  # Changed to int since we're using internal_id
    expectedAnswer: Optional[str]


class Question(BaseModel):
    text: str
    type: str
    internal_id: Optional[int] = None
    condition: Optional[Condition] = None
    options: Optional[List[str]] = []
    image: Optional[str] = None
    scale_points: Optional[int] = None
    imageName: Optional[str] = None


class SurveyDirectCreate(BaseModel):
    adminPassword: str
    title: str
    questions: List[Question]
