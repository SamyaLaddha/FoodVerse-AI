import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# PostgreSQL if DATABASE_URL is set, otherwise SQLite so the demo runs with zero setup.
DATABASE_URL = os.getenv("DATABASE_URL", "").strip() or "sqlite:///./foodverse.db"
args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=args)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
