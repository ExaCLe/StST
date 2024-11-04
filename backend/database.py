from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

DATABASE_URI = os.getenv("DATABASE_URI")
print(DATABASE_URI)
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
