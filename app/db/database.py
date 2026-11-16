import os
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not defined in the environment")

class Base(DeclarativeBase):
    pass