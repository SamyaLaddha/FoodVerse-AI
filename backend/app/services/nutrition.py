"""DEMO nutrition lookup (per typical serving). Replace with a real nutrition API later."""
DATA = {
    "Pizza": (285, 12, 36, 10, 65), "Burger": (354, 17, 30, 18, 48), "Salad": (120, 4, 12, 7, 92),
    "Biryani": (290, 12, 38, 10, 66), "Pasta": (220, 8, 43, 1.3, 70), "Pancakes": (227, 6, 28, 10, 52),
    "Sushi": (200, 9, 38, 1, 80), "Dosa": (168, 4, 29, 3.7, 78), "Samosa": (262, 4, 24, 17, 38),
    "Fruit Bowl": (95, 1, 24, 0.3, 96),
}


def get_nutrition(food_name: str) -> dict:
    key = next((k for k in DATA if k.lower() == food_name.strip().lower()), None)
    c, p, cb, f, s = DATA.get(key, (250, 8, 30, 9, 60))
    return {"food_name": key or food_name.title(), "calories": c, "protein": p, "carbs": cb,
            "fat": f, "health_score": s, "label": "AI-based estimated nutrition (per serving, approximate)"}
