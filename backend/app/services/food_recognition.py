"""DEMO food recognition. Replace recognize_food() with a real model
(e.g. a Hugging Face image-classification model) later; the return shape stays the same."""
import hashlib

FOODS = ["Pizza", "Burger", "Salad", "Biryani", "Pasta", "Pancakes", "Sushi", "Dosa", "Samosa", "Fruit Bowl"]


def recognize_food(image_bytes: bytes, filename: str = "") -> dict:
    name = filename.lower()
    for f in FOODS:
        if f.lower().split()[0] in name:          # filename hint, e.g. "pizza.jpg"
            return {"food_name": f, "confidence": 0.94}
    h = int(hashlib.md5(image_bytes).hexdigest(), 16)  # same image -> same result
    return {"food_name": FOODS[h % len(FOODS)], "confidence": round(0.82 + (h % 15) / 100, 2)}
