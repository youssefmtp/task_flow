# app/db/database.py

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not defined")

# 1. Connection Engine Creation
engine = create_engine(DATABASE_URL)

# 2. Session Manufacturer Creation
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# 3. Models Base Class
class Base(DeclarativeBase):
    pass