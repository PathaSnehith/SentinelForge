from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import services
from .database import init_db
from .models import Alert, LogEntry

app = FastAPI(title="SentinelForge SOC", version="1.0.0")
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
DATA_DIR = BASE_DIR / "data"

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/")
def dashboard() -> FileResponse:
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Dashboard not available.")
    return FileResponse(index_path)


@app.get("/logs", response_model=list[LogEntry])
def get_logs(limit: int = 200) -> list[LogEntry]:
    return services.load_logs(limit=limit)


@app.get("/alerts", response_model=list[Alert])
def get_alerts() -> list[Alert]:
    return services.load_alerts()


@app.post("/ingest")
def ingest(payload: list[dict]) -> dict:
    if not payload:
        raise HTTPException(status_code=400, detail="No log entries provided.")
    alerts = services.ingest_logs(payload)
    return {"ingested": len(payload), "alerts_generated": len(alerts)}


@app.get("/demo/datasets")
def list_datasets() -> dict:
    """List all available datasets in the data directory."""
    datasets = []
    if DATA_DIR.exists():
        for file in sorted(DATA_DIR.glob("*.json")):
            try:
                data = json.loads(file.read_text(encoding="utf-8"))
                datasets.append({
                    "filename": file.name,
                    "name": file.stem.replace("_", " ").title(),
                    "event_count": len(data) if isinstance(data, list) else 0,
                })
            except Exception:
                continue
    return {"datasets": datasets}


@app.post("/demo/ingest-sample")
def ingest_sample_dataset() -> dict:
    sample_path = DATA_DIR / "sample_logs.json"
    if not sample_path.exists():
        raise HTTPException(status_code=404, detail="Sample dataset missing.")
    alerts = services.ingest_from_file(str(sample_path))
    return {
        "message": "Sample dataset ingested.",
        "ingested": len(json.loads(sample_path.read_text(encoding="utf-8"))),
        "alerts_generated": len(alerts),
    }


@app.post("/demo/ingest-dataset/{filename}")
def ingest_dataset(filename: str) -> dict:
    """Ingest a specific dataset by filename."""
    dataset_path = DATA_DIR / filename
    if not dataset_path.exists() or not filename.endswith(".json"):
        raise HTTPException(status_code=404, detail=f"Dataset '{filename}' not found.")
    alerts = services.ingest_from_file(str(dataset_path))
    data = json.loads(dataset_path.read_text(encoding="utf-8"))
    return {
        "message": f"Dataset '{filename}' ingested successfully.",
        "ingested": len(data) if isinstance(data, list) else 0,
        "alerts_generated": len(alerts),
    }

