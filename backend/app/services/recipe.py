"""Rule-based cooking assistant. Replace with an LLM call later."""
RECIPES = {
    "Paneer Masala": dict(ing=["paneer", "tomato", "onion", "ginger", "garlic", "garam masala", "oil", "salt"],
        time="30 min", steps=["Heat oil and saute chopped onion until golden.", "Add ginger-garlic paste and cook 1 minute.",
        "Add pureed tomato, salt and spices; cook until oil separates.", "Add paneer cubes and 1/2 cup water; simmer 5 minutes.",
        "Garnish with coriander and serve hot."], tips=["Soak paneer in warm water for softer cubes.", "Add cream for a richer gravy."]),
    "Vegetable Fried Rice": dict(ing=["rice", "carrot", "beans", "onion", "soy sauce", "oil", "salt"], time="20 min",
        steps=["Use cold, cooked rice.", "Stir-fry chopped vegetables on high heat for 3 minutes.", "Add rice and soy sauce; toss for 3 minutes.",
        "Season and serve."], tips=["Day-old rice gives separate grains."]),
    "Tomato Omelette": dict(ing=["egg", "tomato", "onion", "oil", "salt"], time="10 min",
        steps=["Beat eggs with salt.", "Saute onion and tomato for 2 minutes.", "Pour in eggs and cook until set.", "Fold and serve."],
        tips=["Add green chilli for spice."]),
    "Aloo Gobi": dict(ing=["potato", "cauliflower", "onion", "tomato", "turmeric", "oil", "salt"], time="35 min",
        steps=["Saute onion and tomato with spices.", "Add potato and cauliflower pieces.", "Cover and cook on low heat until soft.", "Serve with roti."],
        tips=["Cut potato and cauliflower to similar sizes."]),
    "Pasta Arrabbiata": dict(ing=["pasta", "tomato", "garlic", "chilli", "olive oil", "salt"], time="20 min",
        steps=["Boil pasta until al dente.", "Saute garlic and chilli in oil.", "Add tomato and simmer 8 minutes.", "Toss pasta in the sauce."],
        tips=["Save a little pasta water to loosen the sauce."]),
}


def _has(words, ing):
    return any(w in ing or ing in w for w in words)


def suggest_recipe(query: str) -> dict:
    q = query.lower().strip()
    for name, r in RECIPES.items():                      # dish name match
        if q and q in name.lower():
            return _out(name, r, [])
    words = [w.strip() for w in q.replace(" and ", ",").split(",") if w.strip()]
    best, score = None, 0
    for name, r in RECIPES.items():                      # ingredient overlap
        s = sum(1 for w in words if _has([w], " ".join(r["ing"])) or any(w in i for i in r["ing"]))
        if s > score:
            best, score = name, s
    if best:
        r = RECIPES[best]
        return _out(best, r, [i for i in r["ing"] if not _has(words, i)])
    return {"dish": "Simple Veg Stir-fry", "ingredients": words + ["oil", "salt", "spices"], "missing": [],
            "steps": ["Chop everything evenly.", "Heat oil and stir-fry on high heat.", "Season and cook until tender."],
            "cooking_time": "15 min", "tips": ["Add a splash of lemon at the end."], "note": "No exact match; generic recipe suggested."}


def _out(name, r, missing):
    return {"dish": name, "ingredients": r["ing"], "missing": missing, "steps": r["steps"],
            "cooking_time": r["time"], "tips": r["tips"], "note": "AI-generated suggestion."}
