# schemas.py
from pydantic import BaseModel, Field
from typing import List, Any, Optional


class ImageMarker(BaseModel):
    x: int
    y: int
    color: str
    text: str


class ImageAnswer(BaseModel):
    markers: List[ImageMarker]


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
    markerLabels: Optional[List[str]] = None  # Add this for image marker labels
    referenceImage: Optional[str] = None  # Add this for reference images
    referenceImageName: Optional[str] = None  # Add this for reference image names
    required: Optional[bool] = False  # Add this line


class SurveyDirectCreate(BaseModel):
    adminPassword: str
    title: str
    questions: List[Question]
