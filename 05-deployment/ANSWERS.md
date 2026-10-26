# Homework 5 — answers and verification

| Question | Result |
| --- | --- |
| Q1: uv version | Record your own `uv --version`; not graded. Verification environment used uv 0.13.4. |
| Q2: locked scikit-learn version | **1.7.2** |
| Q3: direct inference | **0.533** |
| Q4: local API inference | **0.770** |
| Q5: Python base-image tag | **python:3.11.15-slim-bookworm** |
| Q6: container inference | **0.770 expected; run Docker locally to verify** |

## Computed results

Q3 conversion probability, before rounding: `0.5329944186432507`.

Q4 was checked through actual HTTP requests to the provided Uvicorn/FastAPI service:

```json
{"conversion_probability": 0.769799, "conversion": true}
```

The health endpoint returned status `ok`, the expected model SHA-256, and the
expected feature-default SHA-256. Repeated requests produced identical results.
The provided `smoke_test.py` passed, and the provided `q6_test.py` passed against
the **local API**. That client run does not constitute a Docker test.

The reference Dockerfile uses the same model and API, so Q6 is expected to match
Q4. Docker is unavailable in the environment that prepared this solution; a
container build/run has **not** been performed here. Follow `START_HERE_RU.md`
to complete that part on your computer before submitting.

## Reproducibility

- Python: `3.11.15`.
- scikit-learn: `1.7.2`.
- Installed with `uv sync --locked`; the lockfile was not regenerated.
- Used the downloaded frozen artifact; the model was not retrained.
- Model SHA-256: `1646bbdcd38d4f044da6b630c5b332c93a314245a8c21929011c42de51f629f1`.
- Machine-readable observed results: `verification_results.json`.

The supplied upstream files, including Dockerfile, pyproject.toml, uv.lock,
pipeline.bin, training script, and API, are unchanged. `upstream_manifest.json`
records their source paths and hashes.

## Solution files

- `q3_predict.py`: checksum-checked pickle loading and direct prediction for Q3.
- `verify_release.py`: artifact/default checksums, Python version, and dependency checks.
- `verify_api.py`: checks both endpoints, response types, checksum, and repeated inference.
- `START_HERE_RU.md`: Windows CMD instructions, local API, Docker, and submission.
- `README.md`, `homework.md`, and the other reference files: original course release.

This deployment homework uses a separate locked environment. The shared
requirements.txt used for Homework 4 does not need to be changed.
