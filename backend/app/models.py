from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), default="Demo User")
    email = Column(String(120), unique=True, default="demo@foodverse.app")


class FoodAnalysis(Base):
    __tablename__ = "food_analyses"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), default=1)
    filename = Column(String(200))
    food_name = Column(String(100))
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class NutritionResult(Base):
    __tablename__ = "nutrition_results"
    id = Column(Integer, primary_key=True)
    analysis_id = Column(Integer, ForeignKey("food_analyses.id"), nullable=True)
    food_name = Column(String(100))
    calories = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    fat = Column(Float)
    health_score = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


class FreshnessResult(Base):
    __tablename__ = "freshness_results"
    id = Column(Integer, primary_key=True)
    filename = Column(String(200))
    status = Column(String(40))
    confidence = Column(Float)
    explanation = Column(Text)
    recommendation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class HygieneAnalysis(Base):
    __tablename__ = "hygiene_analyses"
    id = Column(Integer, primary_key=True)
    filename = Column(String(200))
    score = Column(Integer)
    observations = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class MealPlan(Base):
    __tablename__ = "meal_plans"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), default=1)
    goal = Column(String(40))
    diet = Column(String(40))
    days = Column(Integer)
    target_calories = Column(Integer)
    plan = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
