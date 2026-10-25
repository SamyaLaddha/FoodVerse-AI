# FoodVerse: Project Documentation Pack

## 1. Architecture
```
React + Vite (frontend)
        |  HTTP / JSON
FastAPI routes  (backend/app/routes/api.py)
        |
Service layer   (backend/app/services/*.py)  <- mock AI, swappable for real models
        |
SQLAlchemy ORM  (backend/app/models.py)
        |
PostgreSQL (or SQLite fallback)
```

## 2. Database schema
| Table | Purpose | Key columns |
|---|---|---|
| users | Demo user | id, name, email |
| food_analyses | Each uploaded image | id, user_id, filename, food_name, confidence, created_at |
| nutrition_results | Estimated nutrition | id, analysis_id (FK), food_name, calories, protein, carbs, fat, health_score |
| freshness_results | Freshness checks | id, filename, status, confidence, explanation, recommendation |
| hygiene_analyses | Kitchen video results | id, filename, score, observations (JSON) |
| meal_plans | Generated plans | id, user_id, goal, diet, days, target_calories, plan (JSON) |

## 3. Features
1. Food recognition: image in, food name and confidence out.
2. Nutrition: estimated calories, protein, carbs, fat, health score.
3. Freshness: Fresh / Moderately Fresh / Possibly Spoiled with explanation and safety advice.
4. Hygiene: video in, score and five indicators out (simulated).
5. Cooking assistant: dish name or ingredients to recipe, steps, time, tips.
6. Meal planner: goal-based 1-day or 7-day plan.
7. Dashboard: totals, recent calories, latest freshness, hygiene and meal plan.

## 4. AI approach and honesty
Services use deterministic demo logic (same file gives same result) behind interfaces such as `recognize_food(image_bytes, filename)`. Future upgrades: Hugging Face image classifier (food recognition), Nutritionix or USDA API (nutrition), YOLO on video frames (hygiene), an LLM (recipes and meal plans). Wording used: "AI-based estimated nutrition", "visual freshness classification", "AI-generated recommendation".

## 5. Testing
| ID | Test | Steps | Expected |
|---|---|---|---|
| T1 | Health | GET /health | {"status":"ok"} |
| T2 | Food recognition | Upload pizza.jpg to /analyze-image | Pizza, 94%, nutrition included |
| T3 | Nutrition | POST /nutrition {"food_name":"Burger"} | 354 kcal |
| T4 | Freshness | Upload image to /freshness | One of three statuses plus advice |
| T5 | Hygiene | Upload video to /hygiene | Score and 5 observations |
| T6 | Recipe | POST /recipe "Paneer, tomato, onion" | Paneer Masala |
| T7 | Meal plan | POST /meal-plan days=7 | 7 days, disclaimer present |
| T8 | Dashboard | GET /dashboard | Totals reflect saved records |
| T9 | UI flow | Use every page in browser | No errors, results displayed |
All endpoints were smoke-tested with FastAPI TestClient; the frontend production build succeeds.

## 6. Project report content
**Abstract.** FoodVerse is a multimodal food intelligence platform that accepts images, video and text to provide food recognition, estimated nutrition, visual freshness classification, kitchen hygiene assessment, cooking guidance and personalized meal plans through a web interface.
**Problem.** Food information is scattered; people lack quick tools to understand what they eat, whether it looks fresh, and how to plan meals; restaurants lack simple hygiene monitoring.
**Objectives.** Build an integrated platform; provide estimated nutrition and freshness insights; simulate hygiene monitoring; offer recipe and meal guidance; store history.
**Methodology.** Agile, phase by phase: setup, recognition and nutrition, freshness, hygiene, cooking, planner, dashboard, testing.
**Tech stack.** Python, FastAPI, SQLAlchemy, PostgreSQL, React, Vite, JavaScript, CSS, Git.
**Limitations.** AI modules are demo implementations; nutrition is approximate; freshness is visual only; no user authentication.
**Future scope.** Real CNN/transformer models, nutrition APIs, video analytics, login, mobile app, allergy detection.
**Conclusion.** FoodVerse shows a modular architecture where AI components can be upgraded independently.

## 7. PPT content (10 slides)
1. Title: FoodVerse, Multimodal Food Intelligence Platform
2. Problem statement
3. Objectives
4. System architecture (diagram above)
5. Technology stack
6. Features: recognition, nutrition, freshness
7. Features: hygiene, cooking, meal planner
8. Database design
9. Demo screenshots and testing
10. Limitations, future scope, thank you

## 8. Viva questions and answers
1. **Why FastAPI?** Fast, type-checked, automatic Swagger docs.
2. **What is the service layer?** Code between routes and database holding the logic, so AI models can be swapped without touching routes.
3. **Is the AI real?** The modules are demo implementations with real interfaces; they can be replaced with pretrained models. We state this openly.
4. **Why PostgreSQL?** Reliable relational database with JSON support.
5. **What is SQLAlchemy?** An ORM mapping Python classes to tables.
6. **Can images give exact calories?** No. Values are estimates; portion size and ingredients are unknown.
7. **Can freshness be proven from a photo?** No. It is a visual classification only; smell, texture and storage also matter.
8. **How would you make hygiene analysis real?** Sample video frames and run an object detector for caps and gloves.
9. **What is CORS?** Browser rule controlling cross-origin requests; enabled so React can call FastAPI.
10. **How does the frontend talk to the backend?** fetch() calls to REST endpoints returning JSON.
11. **What is Vite?** A fast React build tool and dev server.
12. **How is the meal plan generated?** Rule-based: calorie target adjusted by goal and age, meals chosen from diet-specific pools.
13. **Future improvements?** Real models, authentication, allergy checks, mobile app.

## 9. Demo script (5 minutes)
1. Open Home: introduce the name and purpose (30s).
2. Food Analysis: upload pizza.jpg, show food, confidence, estimated nutrition and the estimate label (60s).
3. Freshness: upload an image, show status and safety advice (45s).
4. Hygiene: upload a short video, show score and observations (45s).
5. Cooking Assistant: enter "Paneer, tomato, onion" (30s).
6. Meal Planner: fill the form, generate 7 days (45s).
7. Dashboard: show history updated (30s).
8. Open http://localhost:8000/docs to show Swagger (20s).
9. Close with limitations and future scope (15s).

## 10. Resume description
**FoodVerse: Multimodal Food Intelligence Platform** | Python, FastAPI, SQLAlchemy, PostgreSQL, React, Vite
- Built a full-stack web platform for food recognition, estimated nutrition, visual freshness classification, kitchen hygiene scoring, recipe suggestions and personalized meal plans.
- Designed a layered REST API (routes, services, ORM) with six relational tables and Swagger documentation.
- Created a responsive React dashboard with upload flows, progress indicators and history; designed AI services as swappable modules.
