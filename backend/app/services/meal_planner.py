"""Rule-based meal planner. Replace with an LLM/nutrition engine later."""
MEALS = {
    "veg": {"Breakfast": ["Oats with fruit", "Vegetable poha", "Besan chilla", "Idli with sambar", "Paneer sandwich"],
            "Lunch": ["Dal, rice and salad", "Roti with mixed veg", "Rajma bowl", "Paneer wrap", "Vegetable khichdi"],
            "Snack": ["Roasted chana", "Fruit bowl", "Sprouts chaat", "Buttermilk and nuts"],
            "Dinner": ["Vegetable soup and roti", "Tofu stir-fry", "Palak paneer with roti", "Lentil soup with salad"]},
    "non-veg": {"Breakfast": ["Egg omelette with toast", "Boiled eggs and fruit", "Oats with milk", "Chicken sandwich"],
                "Lunch": ["Grilled chicken with rice", "Fish curry and roti", "Egg curry with rice", "Chicken salad bowl"],
                "Snack": ["Boiled egg", "Fruit bowl", "Roasted chana", "Yogurt and nuts"],
                "Dinner": ["Grilled fish with veggies", "Chicken soup", "Tandoori chicken with salad", "Egg bhurji with roti"]},
}
ADJ = {"Weight loss": -400, "Weight gain": 400, "Maintenance": 0, "Healthy eating": -100}
SLOTS = {2: ["Lunch", "Dinner"], 3: ["Breakfast", "Lunch", "Dinner"], 4: ["Breakfast", "Lunch", "Snack", "Dinner"],
         5: ["Breakfast", "Snack", "Lunch", "Snack", "Dinner"]}


def generate_plan(age, goal, diet, preferences, meals_per_day, days):
    target = max(1400, 2000 + ADJ.get(goal, 0) - (150 if age > 50 else 0))
    pool = MEALS["non-veg" if diet.lower().startswith("non") else "veg"]
    slots = SLOTS.get(meals_per_day, SLOTS[3])
    pref = [p.strip().lower() for p in preferences.split(",") if p.strip()]
    plan = []
    for d in range(days):
        row = []
        for i, slot in enumerate(slots):
            opts = pool[slot]
            liked = [o for o in opts if any(p in o.lower() for p in pref)] or opts
            row.append({"meal": slot, "item": liked[(d + i) % len(liked)],
                        "calories": round(target / len(slots) / 10) * 10})
        plan.append({"day": d + 1, "meals": row})
    return {"goal": goal, "diet": diet, "target_calories": target, "plan": plan,
            "disclaimer": "This is a general AI-generated suggestion and not professional medical or nutrition advice."}
