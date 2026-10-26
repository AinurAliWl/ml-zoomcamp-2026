"""Verify the frozen artifact, missing-value defaults, and locked environment."""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
import tomllib

import sklearn

BASE = Path(__file__).resolve().parent
EXPECTED_MODEL_SHA256 = "1646bbdcd38d4f044da6b630c5b332c93a314245a8c21929011c42de51f629f1"


def verify_release() -> dict:
    metadata = json.loads((BASE / "model_metadata.json").read_text(encoding="utf-8"))
    model_hash = hashlib.sha256((BASE / "pipeline.bin").read_bytes()).hexdigest()
    defaults_hash = hashlib.sha256((BASE / "feature_defaults.json").read_bytes()).hexdigest()
    assert model_hash == EXPECTED_MODEL_SHA256 == metadata["model_sha256"]
    assert defaults_hash == metadata["feature_defaults_sha256"]
    assert json.loads((BASE / "feature_defaults.json").read_text()) == metadata["numeric_defaults"]

    project = tomllib.loads((BASE / "pyproject.toml").read_text())
    lock = tomllib.loads((BASE / "uv.lock").read_text())
    locked_sklearn = next(p["version"] for p in lock["package"] if p["name"] == "scikit-learn")
    assert f"scikit-learn=={locked_sklearn}" in project["project"]["dependencies"]
    assert sklearn.__version__ == locked_sklearn == metadata["scikit_learn"] == "1.7.2"
    assert platform.python_version() == "3.11.15", "Use uv sync --locked with the provided .python-version."
    return {
        "python": platform.python_version(),
        "scikit_learn": sklearn.__version__,
        "model_sha256": model_hash,
        "feature_defaults_sha256": defaults_hash,
        "status": "ok",
    }


if __name__ == "__main__":
    print(json.dumps(verify_release(), indent=2))
