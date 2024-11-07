from dotenv import load_dotenv

load_dotenv()


import os
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Survey, Response, Image
from database import get_db
from schemas import SurveyCreate, ResponseCreate
import csv
from email.mime.text import MIMEText
import smtplib
import base64
from sqlalchemy.orm import joinedload  # Import for eager loading

from survey_processing import create_results_package

app = FastAPI()

# CORS configuration
origins = [os.getenv("FRONTEND_URL")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URI = os.getenv("DATABASE_URI")
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# Email function
def send_email(email: str, text: str):
    msg = MIMEText(text)
    msg["Subject"] = "Survey Results"
    msg["From"] = f"no-reply@{os.getenv('FRONTEND_URL')}"
    msg["To"] = email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("stst.surveys@gmail.com", os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)


@app.post("/api/upload-survey")
async def upload_survey(
    name: str = Form(...),
    password: str = Form(...),
    csv_file: UploadFile = File(...),
    images: List[UploadFile] = File(None),
    db=Depends(get_db),
):
    if password != os.getenv("ADMIN_PASSWORD"):
        raise HTTPException(status_code=403, detail="Invalid password")

    # Read CSV file and parse questions
    content = await csv_file.read()
    decoded = content.decode("utf-8").splitlines()
    reader = csv.DictReader(decoded)
    questions = []
    for row in reader:
        question = {
            "text": row["question"],
            "type": row["answer_type"],
        }
        if question["type"] == "MultipleChoice":
            question["options"] = [
                row["option1"],
                row["option2"],
                row.get("option3"),
                row.get("option4"),
            ]
        elif question["type"] == "ImageQuestion":
            question["imageName"] = row["image_name"]
        elif question["type"] == "LikertScale":
            question["scale"] = int(row["scale_points"])
        questions.append(question)

    # Create survey entry
    survey = Survey(name=name, questions=questions)
    db.add(survey)
    db.commit()
    db.refresh(survey)  # Refresh to get the survey ID

    # Save each image with a UUID
    if images:
        for image in images:
            image_data = await image.read()
            image_record = Image(
                survey_id=survey.id,
                image_data=image_data,
                image_name=image.filename,  # Save original name or label if needed
            )
            db.add(image_record)
        db.commit()

    return {"message": "Survey with images uploaded successfully"}


@app.get("/api/survey/{name}")
async def get_survey(name: str, db=Depends(get_db)):
    survey = (
        db.query(Survey)
        .options(joinedload(Survey.images))
        .filter(Survey.name == name)
        .first()
    )
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    # Convert each image's binary data to base64
    survey_data = {
        "name": survey.name,
        "questions": survey.questions,
        "images": [
            {
                "id": str(image.id),  # UUID as string
                "name": image.image_name,
                "data": base64.b64encode(image.image_data).decode("utf-8"),
            }
            for image in survey.images
        ],
    }

    return survey_data


@app.get("/api/surveys")
async def list_surveys(db=Depends(get_db)):
    surveys = db.query(Survey).all()
    survey_names = [survey.name for survey in surveys]
    return {"surveys": survey_names}


@app.post("/api/survey/{name}/response")
async def save_response(name: str, response: ResponseCreate, db=Depends(get_db)):
    survey = db.query(Survey).filter(Survey.name == name).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    new_response = Response(survey_id=survey.id, answers=response.answers)
    db.add(new_response)
    db.commit()
    return {"message": "Response saved successfully"}


@app.post("/api/request-results")
async def request_results(
    survey_name: str = Form(...),
    password: str = Form(...),
    db=Depends(get_db),
):
    if password != os.getenv("ADMIN_PASSWORD"):
        raise HTTPException(status_code=403, detail="Invalid password")

    print(f"\nProcessing results request for survey: {survey_name}")

    survey = db.query(Survey).filter(Survey.name == survey_name).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    responses = db.query(Response).filter(Response.survey_id == survey.id).all()
    images = db.query(Image).filter(Image.survey_id == survey.id).all()

    return create_results_package(survey, responses, images)


@app.delete("/api/delete-survey/{name}")
async def delete_survey(name: str, password: str, db=Depends(get_db)):
    if password != os.getenv("ADMIN_PASSWORD"):
        raise HTTPException(status_code=403, detail="Invalid password")

    survey = db.query(Survey).filter(Survey.name == name).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    # Delete associated responses and images
    db.query(Response).filter(Response.survey_id == survey.id).delete()
    db.query(Image).filter(Image.survey_id == survey.id).delete()
    db.delete(survey)
    db.commit()

    return {"message": f"Survey '{name}' deleted successfully"}
