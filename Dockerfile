FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install --no-cache-dir .

COPY configs ./configs
COPY scripts ./scripts

# Weights are gitignored. Mount models/plate_detector.pt at runtime.
# OCR is optional: pip install ".[ocr]"
CMD ["python", "scripts/run.py", "--no-display"]
