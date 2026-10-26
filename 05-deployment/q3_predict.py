"""Question 3: load the checked-in pipeline and predict one lead."""
from __future__ import annotations

import json
import pickle
from pathlib import Path

from model import normalize_record
from verify_release import verify_release

LEAD = {
    "lead_source": "paid_ads",
    "industry": "technology",
    "employment_status": "employed",
    "location": "north_america",
    "number_of_courses_viewed": 2,
    "annual_income": 79276.0,
    "interaction_count": 4,
    "lead_score": 0.41,
}


def predict_q3() -> dict:
    verify_release()
    with Path(__file__).with_name("pipeline.bin").open("rb") as model_file:
        pipeline = pickle.load(model_file)
    probability = float(pipeline.predict_proba([normalize_record(LEAD)])[0, 1])
    assert 0 <= probability <= 1
    return {
        "conversion_probability": probability,
        "conversion": probability >= 0.5,
        "answer_q3": f"{probability:.3f}",
    }


if __name__ == "__main__":
    print(json.dumps(predict_q3(), indent=2))
