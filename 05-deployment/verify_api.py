"""Check the running local API or Docker API without third-party client packages."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen

LEAD = {
    "lead_source": "organic_search",
    "industry": "technology",
    "employment_status": "employed",
    "location": "europe",
    "number_of_courses_viewed": 4,
    "annual_income": 80304.0,
    "interaction_count": 7,
    "lead_score": 0.74,
}


def verify_api(base_url: str = "http://localhost:9696") -> dict:
    base_url = base_url.rstrip("/")
    metadata = json.loads(Path(__file__).with_name("model_metadata.json").read_text(encoding="utf-8"))
    with urlopen(base_url + "/health", timeout=15) as response:
        health = json.load(response)
    assert health["status"] == "ok"
    assert health["model_sha256"] == metadata["model_sha256"]
    assert health["feature_defaults_sha256"] == metadata["feature_defaults_sha256"]

    def post_lead() -> dict:
        request = Request(
            base_url + "/predict",
            data=json.dumps(LEAD).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=15) as response:
            return json.load(response)

    result = post_lead()
    assert set(result) == {"conversion_probability", "conversion"}
    probability = result["conversion_probability"]
    assert isinstance(probability, (int, float)) and not isinstance(probability, bool)
    assert 0 <= probability <= 1
    assert isinstance(result["conversion"], bool)
    assert result["conversion"] == (probability >= 0.5)
    assert result == post_lead(), "Repeated inference changed."
    return {"base_url": base_url, "health": health, "prediction": result, "rounded_probability": f"{probability:.3f}"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://localhost:9696")
    args = parser.parse_args()
    print(json.dumps(verify_api(args.base_url), indent=2))
