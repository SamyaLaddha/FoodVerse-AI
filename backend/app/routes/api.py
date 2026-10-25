from fastapi import APIRouter, Depends, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models as m
from ..services.food_recognition import recognize_food
from ..services.nutrition import get_nutrition
from ..services.freshness import analyze_freshness
from ..services.hygiene import analyze_hygiene
from ..services.recipe import suggest_recipe
from ..services.meal_planner import generate_plan

router = APIRouter()


class NutritionIn(BaseModel):
    food_name: str


class RecipeIn(BaseModel):
    query: str


class MealPlanIn(BaseModel):
    age: int = 21
    goal: str = "Healthy eating"
    diet: str = "Vegetarian"
    preferences: str = ""
    meals_per_day: int = 3
    days: int = 1


def _save_nutrition(db, n, analysis_id=None):
    db.add(m.NutritionResult(analysis_id=analysis_id, food_name=n["food_name"], calories=n["calories"],
                             protein=n["protein"], carbs=n["carbs"], fat=n["fat"], health_score=n["health_score"]))


@router.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    data = await file.read()
    rec = recognize_food(data, file.filename or "")
    row = m.FoodAnalysis(filename=file.filename, food_name=rec["food_name"], confidence=rec["confidence"])
    db.add(row); db.flush()
    nutri = get_nutrition(rec["food_name"])
    _save_nutrition(db, nutri, row.id)
    db.commit()
    return {"id": row.id, **rec, "nutrition": nutri}


@router.post("/nutrition")
def nutrition(body: NutritionIn, db: Session = Depends(get_db)):
    n = get_nutrition(body.food_name)
    _save_nutrition(db, n); db.commit()
    return n


@router.post("/freshness")
async def freshness(file: UploadFile = File(...), db: Session = Depends(get_db)):
    r = analyze_freshness(await file.read())
    db.add(m.FreshnessResult(filename=file.filename, status=r["status"], confidence=r["confidence"],
                             explanation=r["explanation"], recommendation=r["recommendation"]))
    db.commit()
    return r


@router.post("/hygiene")
async def hygiene(file: UploadFile = File(...), db: Session = Depends(get_db)):
    r = analyze_hygiene(await file.read())
    db.add(m.HygieneAnalysis(filename=file.filename, score=r["score"], observations=r["observations"]))
    db.commit()
    return r


@router.post("/recipe")
def recipe(body: RecipeIn):
    return suggest_recipe(body.query)


@router.post("/meal-plan")
def meal_plan(body: MealPlanIn, db: Session = Depends(get_db)):
    r = generate_plan(body.age, body.goal, body.diet, body.preferences, body.meals_per_day, 7 if body.days >= 7 else 1)
    db.add(m.MealPlan(goal=body.goal, diet=body.diet, days=len(r["plan"]), target_calories=r["target_calories"], plan=r["plan"]))
    db.commit()
    return r


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    nut = db.query(m.NutritionResult).order_by(m.NutritionResult.id.desc()).limit(8).all()
    fr = db.query(m.FreshnessResult).order_by(m.FreshnessResult.id.desc()).first()
    hy = db.query(m.HygieneAnalysis).order_by(m.HygieneAnalysis.id.desc()).first()
    mp = db.query(m.MealPlan).order_by(m.MealPlan.id.desc()).first()
    return {
        "totals": {"food_analyses": db.query(m.FoodAnalysis).count(), "freshness_checks": db.query(m.FreshnessResult).count(),
                   "hygiene_reports": db.query(m.HygieneAnalysis).count(), "meal_plans": db.query(m.MealPlan).count()},
        "recent_nutrition": [{"food_name": n.food_name, "calories": n.calories, "health_score": n.health_score} for n in reversed(nut)],
        "latest_freshness": {"status": fr.status, "confidence": fr.confidence} if fr else None,
        "latest_hygiene": {"score": hy.score} if hy else None,
        "latest_meal_plan": {"goal": mp.goal, "target_calories": mp.target_calories, "first_day": mp.plan[0]} if mp else None,
    }
