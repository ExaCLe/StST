from pydantic import BaseModel
from typing import List, Any


class SurveyCreate(BaseModel):
    name: str
    questions: List[Any]


class ResponseCreate(BaseModel):
    answers: dict
