"""DEMO visual freshness classifier. Replace with a real model later."""
import hashlib

LEVELS = [
    ("Fresh", "Colour and surface look consistent with fresh food.",
     "Looks fine visually. Still store it properly and check smell and texture before eating."),
    ("Moderately Fresh", "Some colour or surface changes are visible.",
     "Consume soon and check smell and texture. Refrigerate if not eating immediately."),
    ("Possibly Spoiled", "Visible discolouration or texture changes detected.",
     "Avoid eating if unsure. A photo cannot confirm food safety, so when in doubt, throw it out."),
]


def analyze_freshness(image_bytes: bytes) -> dict:
    h = int(hashlib.sha1(image_bytes).hexdigest(), 16)
    status, expl, rec = LEVELS[h % 3]
    return {"status": status, "confidence": round(0.70 + (h % 25) / 100, 2), "explanation": expl,
            "recommendation": rec, "disclaimer": "Visual freshness classification only. Not a food-safety guarantee."}
