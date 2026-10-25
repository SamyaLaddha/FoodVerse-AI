# FoodVerse: Multimodal Food Intelligence Platform

Analyze food, understand nutrition, assess freshness, evaluate kitchen hygiene, and get personalized meal recommendations.

- 🌐 **Live Demo:** [https://foodverse-ai-djsd.onrender.com/](https://foodverse-ai-djsd.onrender.com/)
- 📖 **API Docs (Swagger):** [https://foodverse-ai-djsd.onrender.com/docs](https://foodverse-ai-djsd.onrender.com/docs)

> AI services are **demo/mock implementations** behind clean service interfaces (`backend/app/services/`). Each can be replaced with a real model later without changing routes or the frontend.


## Run it (2 terminals)

**Terminal 1: backend** (Python 3.10+)
```
cd backend
python -m venv venv
venv\Scripts\activate          # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Swagger docs: http://localhost:8000/docs

**Terminal 2: frontend** (Node 18+)
```
cd frontend
npm install
npm run dev
```
Open http://localhost:5173

## Database
By default it uses a local SQLite file so it works immediately. To use **PostgreSQL**: create a database named `foodverse`, copy `.env.example` to `.env` (project root), and set
`DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/foodverse`. Tables are created automatically on startup.

## Architecture
React (Vite) -> FastAPI routes -> Service layer (mock AI) -> SQLAlchemy -> PostgreSQL

## API
GET `/`, GET `/health`, POST `/analyze-image`, POST `/nutrition`, POST `/freshness`, POST `/hygiene`, POST `/recipe`, POST `/meal-plan`, GET `/dashboard`

## Tables
users, food_analyses, nutrition_results, freshness_results, hygiene_analyses, meal_plans

## Demo tip
Name a food photo `pizza.jpg` (or burger, salad, biryani, dosa...) to get a predictable recognition result.

## Disclaimers
Nutrition values are AI-based estimates. Freshness is a visual classification, not a food-safety guarantee. Hygiene results are simulated. Meal plans are general suggestions, not medical advice.
