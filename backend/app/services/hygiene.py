"""DEMO kitchen hygiene analysis. Replace with real video analysis (e.g. YOLO on sampled frames) later."""
import random

CHECKS = ["Hair cap compliance", "Glove usage", "Food handling", "Kitchen cleanliness", "Cross-contamination risk"]


def analyze_hygiene(video_bytes: bytes) -> dict:
    rng = random.Random(len(video_bytes))     # same file -> same result
    items, total = [], 0
    for c in CHECKS:
        s = rng.randint(55, 98)
        total += s
        items.append({"indicator": c, "score": s, "status": "ok" if s >= 75 else "warn",
                      "note": "No issue detected" if s >= 75 else "Needs attention"})
    return {"score": round(total / len(CHECKS)), "observations": items,
            "disclaimer": "Simulated AI-generated assessment for demonstration. Not an official inspection."}
