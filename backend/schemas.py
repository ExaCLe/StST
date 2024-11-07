from pydantic import BaseModel
from typing import List, Any


class SurveyCreate(BaseModel):
    name: str
    questions: List[Any]


class ResponseCreate(BaseModel):
    answers: dict


class Question(BaseModel):
    text: str
    type: str
    options: List[str] = []
    image: str = None


class SurveyDirectCreate(BaseModel):
    adminPassword: str
    title: str
    questions: List[Question]
