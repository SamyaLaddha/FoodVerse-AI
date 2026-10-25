from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine, SessionLocal
from . import models
from .routes.api import router

Base.metadata.create_all(bind=engine)
with SessionLocal() as db:                      # make sure the demo user exists
    if not db.query(models.User).first():
        db.add(models.User()); db.commit()

app = FastAPI(title="FoodVerse API", description="Multimodal Food Intelligence Platform", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(router)


@app.get("/")
def root():
    return {"name": "FoodVerse", "subtitle": "Multimodal Food Intelligence Platform", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}
